import Control.Applicative
import Control.Monad.IO.Class
import Control.Monad.Reader
import Control.Lens
import Data.ByteString.Lazy qualified as LBS
import Data.Map (Map)
import Data.Map qualified as Map
import Data.Maybe (catMaybes)
import Data.Text (Text)
import Data.Text.Lazy.IO qualified as L

import System.Environment (getArgs)
import GHC.Generics

import Data.Aeson qualified as Aeson
import Data.Aeson.Text qualified as Aeson
import Data.Aeson.Lens
import Data.Yaml qualified as Yaml
import Codec.Archive.Tar qualified as Tar
import Codec.Compression.Lzma qualified as Lzma
import Text.Pandoc as Pandoc


type FieldSpecMap = Map Text FieldSpec
data FieldSpec = FieldSpec
  { fs_value :: Maybe Aeson.Key
  , fs_isDictionary :: Maybe Bool
  , fs_isArray :: Maybe Bool
  , fs_skip :: Maybe Bool
  , fs_desc :: Maybe Text
  , fs_comment :: Maybe Text
  , fs_duplicate :: Maybe Text
  , fs_const :: Maybe Text
  }
  deriving Generic

instance Yaml.FromJSON FieldSpec where
  parseJSON = Aeson.genericParseJSON
    Aeson.defaultOptions
      { Aeson.fieldLabelModifier = drop 3
      , Aeson.rejectUnknownFields = True
      }

data Env = Env
  { fieldSpec :: FieldSpecMap
  }

type App a = ReaderT Env IO a


main :: IO ()
main = do
  -- load/create dictionaries
  args <- getArgs
  case args of
    [] -> error "Not enough arguments"
    specFile : dataFiles -> Yaml.decodeFileEither specFile >>= \case
      Left err -> logErr err
      Right spec -> do
        runReaderT (main' dataFiles) $ Env spec

main' :: [FilePath] -> App ()
main' = mapM_ $ \file -> do
  liftIO (LBS.readFile file)
    >>= processTarEntries . Tar.read . Lzma.decompress

logErr :: (MonadIO m, Show e) => e -> m ()
logErr = error . show

processTarEntries :: Tar.Entries Tar.FormatError -> App ()
processTarEntries = \case
  Tar.Done -> return ()
  Tar.Fail err -> logErr err
  Tar.Next e es -> do
    case Tar.entryContent e of
      Tar.NormalFile str _ -> processFile str
      err -> logErr err
    processTarEntries es

processFile :: LBS.ByteString -> App ()
processFile str =
  case Aeson.eitherDecode str of
    Left err -> logErr err
    Right jsn -> mapM_ processJsonDoc
      $ (jsn :: Aeson.Value)
        ^.. key "searchResult" . key "documents" . values

processJsonDoc :: Aeson.Value -> App ()
processJsonDoc doc = do
  case doc ^? key "id" . _Value of
    Nothing -> logErr ("No id in document" :: Text)
    Just hash -> do
      spec <- asks fieldSpec

      let fields = catMaybes $ map
            (transformField spec)
            (doc ^.. key "additionalFields" . values)
      let res = Map.fromList $ ("id", hash) : fields

      let textFld = "case_user_document_text_tag"
      res' <- case Map.lookup textFld res of
        Nothing -> return res
        Just html -> do
          md <- liftIO $ html2md (html ^. _String)
          return $ Map.insert textFld (Aeson.toJSON md) res

      liftIO $ L.putStrLn $ Aeson.encodeToLazyText res'

transformField :: FieldSpecMap -> Aeson.Value -> Maybe (Text, Aeson.Value)
transformField specMap v = do
  name <- v ^? key "name" . _String
  spec <- Map.lookup name specMap

  let skip = any (== Just True) [
        fs_skip spec,
        const True <$> fs_const spec,
        const True <$> fs_duplicate spec]

  case skip of
    True -> Nothing
    False -> do
      valFld <- fs_value spec <|> Just "value"
      value <- v ^? key valFld . _Value
      return (name, value)

  -- collect isArray

html2md :: Text -> IO Text
html2md str = Pandoc.runIOorExplode
  $ readHtml def
    { readerExtensions = extensionsFromList [Ext_native_spans] }
    str
  >>= writeMarkdown def
    { writerWrapText = WrapNone
    , writerExtensions = pandocExtensions
    }

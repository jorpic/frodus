import Control.Applicative
import Control.Monad.IO.Class
import Control.Monad.Reader
import Control.Lens
import Data.ByteString.Lazy qualified as LBS
import Data.ByteString.Lazy.Char8 qualified as LBS8
import Data.Maybe (fromMaybe)
import Data.Map.Strict (Map)
import Data.Map.Strict qualified as Map
import Data.Set (Set)
import Data.Set qualified as Set
import Data.Text (Text)
import Data.Text qualified as T
import Data.Text.Lazy.IO qualified as L
import Data.Vector qualified as Vec
import Data.IORef (IORef, newIORef, readIORef, modifyIORef)

import System.IO (hPrint, stderr)
import UnliftIO.Exception (throwString, catch, StringException)
import System.Environment (getArgs)
import GHC.Generics

import Data.Aeson qualified as Aeson
import Data.Aeson.Text qualified as Aeson
import Data.Aeson.Lens
import Data.Yaml qualified as Yaml
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
  , fs_html2md :: Maybe Bool
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
  , seenDocsRef :: IORef (Set (Text, Int))
  }

type App a = ReaderT Env IO a

main :: IO ()
main = do
  args <- getArgs
  case args of
    [specFile] -> Yaml.decodeFileEither specFile >>= \case
      Left err -> logErr err
      Right spec -> do
        env <- Env spec <$> newIORef Set.empty
        lns <- LBS8.lines <$> LBS.getContents
        runReaderT (forM_ lns processJson) env
    _ -> error "Usage:\n\t $ transform <FIELD_SPEC>"


processJson :: LBS.ByteString -> App ()
processJson str
  = case Aeson.eitherDecode str of
    Left err -> logErr err
    Right jsn -> mapM_ processJsonDoc
      $ (jsn :: Aeson.Value)
        ^.. key "searchResult" . key "documents" . values

processJsonDoc :: Aeson.Value -> App ()
processJsonDoc doc = do
  case doc ^? key "id" . _Value of
    Nothing -> logErr ("No id in document" :: Text)
    Just hash -> do
      Env {fieldSpec, seenDocsRef} <- ask

      res <- foldM
        (\obj val -> addField fieldSpec obj val
          `catch` \err -> logErr (err :: StringException) >> return obj)
        (Map.singleton "id" hash)
        (doc ^.. key "additionalFields" . values)

      let textLen = fromMaybe 0 $ do
            txt <- Map.lookup "case_user_document_text_tag" res
            T.length <$> txt ^? _String
      let dupKey = (hash ^. _String, textLen)

      liftIO $ do
        seenDocs <- readIORef seenDocsRef
        if Set.member dupKey seenDocs
          then logErr ("skipping duplicate" :: Text, dupKey)
          else do
            modifyIORef seenDocsRef $ Set.insert dupKey
            L.putStrLn $ Aeson.encodeToLazyText res

type Obj = Map Text Aeson.Value

addField :: FieldSpecMap -> Obj -> Aeson.Value -> App Obj
addField specMap obj val = do
  name <- throwNothing
    (val ^? key "name" . _String)
    ("No name in field object" :: Text, val)

  FieldSpec{..} <- throwNothing
    (Map.lookup name specMap)
    ("Unknow field" :: Text, name)

  let skip = fs_skip == Just True
        || fs_const /= Nothing
        || fs_duplicate /= Nothing

  if skip
    then return obj
    else do
      val' <- throwNothing
        (do
          valFld <- fs_value <|> Just "value"
          val ^? key valFld . _Value)
        ("Can't get value" :: Text, val)

      val'' <- case fs_html2md of
        Just True -> liftIO $ Aeson.toJSON <$> html2md (val' ^. _String)
        _ -> pure val'

      let val''' = case fs_isArray of
            Just True -> Aeson.Array
              $ case Map.lookup name obj of
                Just (Aeson.Array xs) -> Vec.snoc xs val''
                _ -> Vec.singleton val''
            _ -> val''

      return $ Map.insert name val''' obj

-- --

html2md :: Text -> IO Text
html2md str = Pandoc.runIOorExplode
  $ readHtml def
    { readerExtensions = extensionsFromList [Ext_native_spans] }
    str
  >>= writeMarkdown def
    { writerWrapText = WrapNone
    , writerExtensions = pandocExtensions
    }

throwNothing :: Show err => Maybe val -> err -> App val
throwNothing Nothing err = throwString $ show err
throwNothing (Just v) _  = pure v

logErr :: (MonadIO m, Show e) => e -> m ()
logErr = liftIO . hPrint stderr

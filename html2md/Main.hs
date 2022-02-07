import Control.Monad ((>=>))
import Data.Aeson qualified as Aeson
import Data.ByteString.Lazy qualified as LBS
import Data.HashMap.Strict qualified as HM
import Text.Pandoc


main :: IO ()
main
  = LBS.getContents
  >>= mapM_ f . filter (/="") . LBS.split 10 -- Char.ord '\n' == 10
  where
    f = either error (convert >=> putLbsLn . Aeson.encode)
      .  Aeson.eitherDecode

putLbsLn :: LBS.ByteString -> IO ()
putLbsLn s = LBS.putStr s >> LBS.putStr "\n"

convert :: Aeson.Value -> IO Aeson.Value
convert = mapObjM
  $ adjustM "case_user_document_text_tag"
  $ mapStrM html2md
  where
    html2md val = runIOorExplode
      $ readHtml def
        { readerExtensions = extensionsFromList [Ext_native_spans] }
        val
      >>= writeMarkdown def
        { writerWrapText = WrapNone
        , writerExtensions = pandocExtensions
        }

    mapObjM f = \case
      Aeson.Object val -> Aeson.Object <$> f val
      val -> pure val -- FIXME: report unexpected value?

    mapStrM f = \case
      Aeson.String val -> Aeson.String <$> f val
      val -> pure val

    adjustM k f m = case HM.lookup k m of
      Just v -> HM.insert k <$> f v <*> pure m
      Nothing -> pure m

import XMonad
import XMonad.Hooks.DynamicLog
import XMonad.Util.Run(spawnPipe)
import XMonad.Util.EZConfig(additionalKeys)
import XMonad.Layout.Spiral as Spiral
import qualified XMonad.StackSet as W
import System.IO

-- Define the names of all workspaces
-- myWorkspaces = ["music", "web", "main", "secondary", "comm"]

-- Define layouts
myLayout = spiral (6/7)

-- Run XMonad
main = xmonad $ defaultConfig
        { modMask = mod4Mask     -- Rebind Mod to the Windows key
--        , workspaces = myWorkspaces -- Name all workspaces
        , manageHook = myManageHook
        , layoutHook = myLayout
        }


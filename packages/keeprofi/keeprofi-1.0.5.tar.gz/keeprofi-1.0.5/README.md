# Keeprofi

Python util that provide fast read-only interface for keepass database using rofi drun menu.

## Usage

1. Just run `keeprofi` command in console. You will see rofi drun menu with your filesystem where you can find and select your keepass database file.
2. Type the password for your keepass database.
3. Select password.

	* Press `Enter` for default action(copy password in clipboard)
	* `Ctrl+Enter` - for additional action(type password in active window)
	* `Shift+Enter` - for open password attributes menu where you can select any attr with `Enter` or `Ctrl+Enter`

## Features

* `Ctrl+h` for switching hidden files in filesystem navigator
* After every succesfull `*.kdb` opening its path saves in cache file. So you don't need to find it every time
* Keeprofi can remember your `*.kdb` file password in system keyring. By default this feature disables. Keeprofi saves only last entered password, so if will try to open new `*.kdb` file keeprofi remove last password and ask you for new.
* Keeprofi sends desktop notifications when you type wrong `*.kdb` file password or copy selected password/attribute in clipboard.

## Configuration

According your system XDG settings keeprofi configuration file can be saved in:

* `~/.keeprofi/config.json`
* or `~/.config/keeprofi/config.json`

Here is default settings with descriptions:

```
{
	"kb": {
		"hidden": "Control+h",             // keybind for switching hidden files
		"custom_action": "Control+Return", // keybind for custom action(typing) by default
		"pass_attrs": "Shift+Return"       // keybind for password attributes menu open
	},
	"icons": {
		"success": "keepassxc-dark",       // notification success icon
		"fail": "keepassxc-locked"         // notification fail icon
	},
	"default_action": "copy",              // ['copy'|'type'] - default action that will done by 'Enter' pressing
	"remember_pass": false,                // [false|true|'1W2D3H4M5S'] - this flag controlles using keyring for `*.kdb` file password saving
	"dir_format": "/{name}"                // format of directories and keepass groups output
}
```

### remember_pass

Can take 3 value:

* `false`(default) - `*.kdb` file password never saves in keyring
* `true` - `*.kdb` file password always saves in keyring
* `1W2D3H4M5S` - time interval format that specify how long password can be stored in keyring. Where:
	* W - weeks
	* D - days
	* H - hours
	* M - minutes
	* S - seconds

	any unit can be missed, but existing units should observe the specified order

## Dependencies

* `rofi`
* `xclip` - copy password in clipboard
* system keyring(optional)

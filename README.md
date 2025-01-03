# make-symlinks

Easy, safe way to create symlinks in the home directory pointing to files in a
given directory. The default mode of operation is a dry run with many prompts.

This is useful if you store your dotfiles in a Sync or Backup folder that gets
synced with the cloud. This script creates symlinks to those files, in the home
directory. You could also have different sets of dotfiles for different
machines.

## Usage

```
python3 make-symlinks.py <source_root> <file1> <file2> ...
```

## Examples

Create symlinks in home dir to all files in `~/Sync/dotfiles`:

```
python3 ./make-symlinks.py ~/Sync/dotfiles
```

Create symlinks in home dir to only certain folders in `~/Sync`:

```
python3 ./make-symlinks.py ~/Sync Code Repos
```

## Alternatives

You could check out GNU stow, but I didn't have a good experience with it. This
script is simple and safe, and you can easily customize it to your liking.

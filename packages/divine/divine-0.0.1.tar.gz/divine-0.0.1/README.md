# Divine

Divine is a configuration utility with unique features:
  - Ability to chain configs together, composing the whole from pieces
  - Ability to quickly grab a nested key using notation like
    c.get('abc/xyz/foo/bar')
  - Integrated f-strings for composable values and DRY patterns
  - Auto-callable config entries to instantiate a class or call a function with args and kwargs automatically from the config (yes, this is a security risk; don't parse any config from unknown sources)

Divine accepts YAML or JSON files. It can be manually configured or auto-configured with an environment variable pointing to a config file. This allows for many processes to use the config without having to explicitly initialize the config in each process.


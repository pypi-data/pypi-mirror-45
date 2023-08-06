# pylingo
https://github.com/antlr/antlr4/blob/master/doc/python-target.md
https://github.com/antlr/antlr4/blob/master/doc/getting-started.md

General purpose extensible configuration language.

```bash

config {
  {key} = { object | array | scalar }
}

import "{name}" {
  version = "~> 1.16"
  module  = "{scalar}"
}

variable "{name}" {
	{key} = { object | array | scalar }
}

data "{source}" "{name}" {
    {key} = { object | array | scalar }
}


#create event log group
generator "{type}" "{name}" {
  {key} = { object | array | scalar }
}



```
#!/usr/bin/env bash

statements() {
  echo "<=== ALL import statements ===>";
                grep -RI -h 'import' --include \*.py . | \  # search all .py files for lines containing `import`
                grep -v '^#' | \                            # respect comments
                uniq -u | \                                 # ignore duplicates
                # NEED A WAY TO HIGHLIGHT `import`, `from`, `as`
                grep --color=auto 'import'

  # echo "$lines"
  # grep -E "(import|from|as)" <<< $lines
}


packages() {
  echo "<=== CAT pip list ===>";

}


requirements() {
  echo "<=== TOUCH requirements ===>";

}


install() {
  echo "<=== INSTALL promiscuous ===>";

}

# procedure
statements

# good
# grep -RI -h 'import' --include \*.py . | grep -v '^#' |  uniq -u

# grep -RI -h 'import' --include \*.py . | grep "^import" | grep -v '^#' |  uniq -u

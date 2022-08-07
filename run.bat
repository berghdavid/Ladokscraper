@ECHO OFF

WHERE /Q python
IF %ERRORLEVEL% NEQ 0 (
  ECHO "Could not find python."
  ECHO "Install python and pip before continuing"
  EXIT /b 0
)

WHERE /Q pip
IF %ERRORLEVEL% NEQ 0 (
  ECHO "Could not find pip."
  ECHO "Install pip before continuing"
  EXIT /b 0
)

pip show selenium -q
IF %ERRORLEVEL% NEQ 0 (
  ECHO "Could not find pip package selenium."
  ECHO "Installing selenium..."
  pip install selenium
)

pip show alive-progress -q
IF %ERRORLEVEL% NEQ 0 (
  ECHO "Could not find pip package alive-progress."
  ECHO "Installing alive-progress..."
  pip install alive-progress
)

python src/main.py

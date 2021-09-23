for %%f in (*.ui) do (
    python -m PyQt5.uic.pyuic -x %%f -o %%~nf.py
    COPY %%~nf.py		..\coin\gui\*.*
    echo UI FileName [%%f] -> PythonFile [%%~nf.py]
)
Pause
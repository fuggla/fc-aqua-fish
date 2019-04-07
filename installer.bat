rem @echo off
for /f %%i in ('python -c "import site; print(site.getsitepackages()[0])"') do set PYTHON_ROOT="%%i"
rem copy C:\Python\Lib\site-packages\arcade\Win64\avbin.dll .
rem copy avbin.dll avbin64.dll
rem pyinstaller --exclude-module tkinter --add-data resources;resources --add-data ./avbin64.dll;. --add-data ./avbin.dll;Win64 --onefile --noconsole fish_vars.py main.py vars.py functions\diagnose_name_gender_attraction_health.py functions\diagnose_name_gender_health_hungry.py functions\loads.py classes\blue_small_fish.py classes\carrot.py classes\fish.py  classes\fps.py classes\plant_blueberry.py classes\popcorn.py classes\purple_fish.py classes\state.py classes\blueberry.py classes\egg_fish.py classes\fish_animate.py classes\hook.py  classes\plant_foreground.py classes\press_q.py classes\shape.py classes\timer.py bubble_map.py classes\fade.py classes\fish_move.py  classes\liquid_assets.py classes\pointer.py  classes\press_space.py classes\shark.py classes\window.py
rem del avbin.dll
rem del avbin64.dll
rem pause
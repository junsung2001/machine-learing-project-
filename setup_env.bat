@echo off
REM 1. Python 3.10이 설치되어 있어야 함 (py -3.10 명령 가능해야 함)

echo [1] 가상환경 생성 중...
py -3.10 -m venv ml_env

echo [2] 가상환경 활성화 중...
call ml_env\Scripts\activate.bat

echo [3] pip 최신화...
python -m pip install --upgrade pip

echo [4] 필수 패키지 설치 중...
pip install flask==3.0.2 ^
    scikit-learn==1.4.2 ^
    joblib==1.3.2 ^
    numpy==1.26.4 ^
    pandas==2.2.2

echo.
echo  환경 구성이 완료되었습니다.
echo 사용하려면: call ml_env\Scripts\activate
pause

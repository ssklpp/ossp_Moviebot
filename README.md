##텔레그램 영화관 챗봇

### Chosun Univ. Computer engineering Kim TaeWan

Windows 10 Pro
Python : 3.6.3
BotHub.Studio
Telegram

/newbot 명령 이용 봇 생성
<img src="https://github.com/ssklpp/ossp_Moviebot/blob/master/image/BotFather.PNG">

[BotHub.Studio](https://app.bothub.studio/) 가입

CLI 도구 설치
```
pip install bothub-cli
```

계정 연결
```
bothub configure
```

프로젝트 폴더 생성
```
mkdir <Folder name>
cd <Folder name>
bothub init
```

텔레그램 Token 연결
```
bothub channel add telegram --api-key=<api-key>
```

서버로 프로젝트 업로드
```
bothub deploy
```


movies.py 파일 작성


영화진응위원회 API key 입력
```
bothub property set box_office_api_key <api-key>
```

bot.py 파일 작성

```
bothub deploy
```

<img src="https://github.com/ssklpp/ossp_Moviebot/blob/master/image/output1.PNG">
<img src="https://github.com/ssklpp/ossp_Moviebot/blob/master/image/output2.PNG">
<img src="https://github.com/ssklpp/ossp_Moviebot/blob/master/image/output3.PNG">
<img src="https://github.com/ssklpp/ossp_Moviebot/blob/master/image/output4.PNG">
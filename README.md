github convention <br/>

backend / frontend / model / data repo로 구분 <br/><br/>

**branch 생성 규칙** <br/>
ex) backend/feat/#14, frontend/fix/#15, model/exp/#12 <br/>
dev branch -> main branch로 pull request하는 방식으로 사용 <br/><br/>

**커밋 규칙** <br/>
ex) [feat] : topic data 생성 API 구현 #19 <br/><br />

**백엔드**<br/>
CLI에서 main이 있는 repo로 이동해서 uvicorn main:app --reload를 입력하면 실행. <br />
database 연결 정보는 보안 문제로 커밋 안했음. src 폴더에서 '.env' 파일 생성해서 써야 함. <br />
backend repo에 'must_read' 파일에 개발 패턴 공유.<br/><br/>

**프론트엔드**<br/>
설치 방법<br />
node.js 20.11.1 version download <br />
npm install -g create-react-app <br /><br />


CLI에서 frontend repo로 이동해서 npm start를 입력해주면 실행. <br /><br />

pages repo에 페이지 생성, 페이지에 필요한 component는 components repo에서 생성해서 가져다 쓰면 됨 <br />
화면에 띄워주려면 라우팅해줘야 하는데 Router.js에 이런 식으로 추가해주면 라우팅 됨. <Route path="/" element={<Allnews />} /> <br />


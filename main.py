# todo app 만들고 도커로 배포
# main.py 만들고 requirements.txt 만들고 dockerfile 만들어서 이미지 생성후 도커허브에 태그를 달아서 푸시함
# AWS EC2 인스턴스에서 도커허브에서 이미지를 풀 받아서 컨테이너 실행
# 방화벽 설정해서 80포트 오픈 후 웹브라우저에서 EC2 퍼블릭 IP로 접속해서 FastAPI 실행 확인
# dbeaver로 테이블 만들고, CRUD 테스트

# be source code 개발
# dockerfile 만들기
# docker image build (in local)
# docker push (in local to dockerhub)
# ec2 instance 발급 & docker 설치
# ec2 docker login & docker pull
# ec2 docker run (postgres + 내 custom image)
# ec2 security group (방화벽 ingress port 허용 5432, 8888)

from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class CreateTodoSchema(BaseModel):
    id:str
    title:str
    content:str

import psycopg2
from psycopg2.extras import RealDictCursor
conn = psycopg2.connect(
    host = 'db-container', 
    port = 5432, 
    database ='postgres', 
    user = 'postgres', 
    password = '1234',
    cursor_factory = RealDictCursor
)
cursor = conn.cursor()
cursor.close() #close the cursor after use


#create
@app.post("/create",status_code = 200)
def create_todo(data:CreateTodoSchema):
    id = data.id
    title = data.title
    content = data.content

    cursor.execute("""
        INSERT INTO todos (id,title,content)
        VALUES (%s, %s, %s) RETURNING *
    """,
    (id,title,content)
    )
    new_data = cursor.fetchone()
    conn.commit()


    return new_data



#read
@app.get("/read",status_code = 200)
def read_data(id:str):
    """test"""

    cursor.execute("""
        SELECT * FROM todos
        WHERE id = %s
    """,
    (id,)
    )
    data = cursor.fetchall()
    return {"data":data}


#update



#delete
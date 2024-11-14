from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
from enum import Enum

#creating an instance of the FastAPI class. Say an object on the app variable
app = FastAPI()

#making a get request
@app.get("/test")

#making a random method as the homepage is blank now

def ind():
    return {"Name":"Antor"}
@app.get("/")

#get method or line er pore first jei function pabe ota get korbe onno gula na

def hello():
    return 9

student={
    1: {
        "name":"a",
        "age":123,
        "class":12
       }
}

#{student_id}=eta use kora hoy user ja input dibe ta {} ta diye replace hoye jabe student_id er jaygay jekono name hote pare eta just hint hisebe use kortechi

#jate user bujhe je ekhane studet id pass korte hobe. Not necessarily function parameter and {vitor} same hote hobe. 

# {} means porer method jeta run korbe setate ei value argument hisebe pass koro

@app.get("/student-data/{student_id}")

#fastapi te always type_hints use kora lagbe function parameter er sathe type obossoi bole dite hobe

def get_stu_info(student_id: int):

    return student[student_id]

#to test call for homeaddress/student-data/1 = 1 er record ta show korbe

@app.get("/student-name/{student_id}")

#type hints = kichu bosano tai path parameter er jonnoi path import kora

#description onek ta placeholder er moto kaj kore UX baranor jonno

def get_stu_name(student_id: int = Path(..., description="Provide the Student ID Number", gt=0, lt=3)):
    return student[student_id]["name"]

#there is lot of things we can do with path parameter we can also include condition on receiving argument
#lt=less than, gt=greater than, le=less than or equals to

#... means this field is mendatory

@app.get("/users/{username}")
def read_user(
    username: str = Path(..., regex="^[a-zA-Z0-9_-]{3,15}$", description="Username must have length 3-15 and only contain a-z,A-Z,0-9,_,-")
):
    return {"username": username}

#regex for regular expression.
#Here, username must be 3-15 characters long and contain only letters, numbers, underscores, or hyphens

#Query Parameter: Endpoint er moddhei action ba query include kore deya. Alada kore {} diye useer er theke input pathano lage na.

#They are appended after a ? in the URL and are separated by & for multiple parameters.

#goolge.com/result?=python ekhane search bar e auto python query pathay tar result page ta caowa hocche etai query parameter see example below

#instead of setting str=None in FastAPI it is best practice to use Optional
#To use optional you should import Optional from Typing

@app.get("/get-student")
def get_name(name: Optional[str]=None):

    for id in student:
        if student[id]["name"]==name:
            return id 
    
    return {name: "not found"}
#str=None dile user kichu input kora charao request sent korte parbe. Orthat this field is not mendatory. 
# But path parameter e kichu na kichu pass kora lagbei endpoint e {} tai argument mendatory kore dey.

#We can also use combination of both path parameter and query parameter

@app.get("/random/{something}")

def combining(something: str, id: Optional[int]=None):
    return {something: id}

#something is the path parameter so Path parameter should be define first in the method then the query parameter.


#Now request body and Post Method part

#for the request body part we have to import BaseModel from Pydantic

#Let's Create a Student class. As python is case sensitive Student and student are not same. 
# Amra basically Student name 1 ta user defined class banabo with the help of BaseModel je student dictionary te new data input dite help korbe.

class Student(BaseModel):
    name: str
    age: int
    year: str

#now we can use post method to insert a new value to the student dictionary with the help of request body
#request body http request er jonno 1 ta sundor structure provide kore jekhane user structural way te value insert kore request korte pare

@app.post("/set-value/{stu_id}")

def set_value(stu_id: int, stu_info: Student):
    if stu_id in student:
        return {"Error":" Student id is already exist"}
    student[stu_id]=stu_info
    return student[stu_id]

#Jehetu post method amr student dictionary te new record add kore
# Sei record already created get request diyeo access kora jabe



#NOW put method. For put method we have to create another BaseModel class jehetu ager Student class post e use korchi ar sob field mendatory chilo

class Update_Stu(BaseModel):
    name: Optional[str]=None
    age: Optional[int]=None
    year: Optional[str]=None

@app.put("/update/{stu_id}")
def update_info(stu_id: int, stu_info: Update_Stu):
    if stu_id not in student:
        return {"Error": "No record present for the provided id"}

    if stu_info.name != None:
        student[stu_id].name=stu_info.name
    
    if stu_info.age != None:
        student[stu_id].age=stu_info.age
    
    if stu_info.year != None:
        student[stu_id].year=stu_info.year

    return student[stu_id]



#Last CRUD method is delete method. Simply deleting any data using del keyword

@app.delete("/delete/{stu_id}")

def delete_student(stu_id: int):

    if stu_id not in student:
        return {"Error":"The student id is not present in the dictionary"}

    del student[stu_id]
    return {"The student is successfully deleted"}

#a very interesting model is enum. enum means enumerator.
# Basically when we use enum it does work like a dropdown menu
# User can't input anything else other than available options defined in enum class
#User ke input er list show kora je er moddhe chose koro er baire kichu chose kora jabe na

class Interesting(str, Enum):
    alex="AAlex"
    bob="bob"
    poncalak="poncalak pandu"

@app.get("/enm/{testing}")

async def enjoy(testing: Interesting):
    if testing is Interesting.alex:
        return {"alex": testing, "Message": "Hi"}
    if testing is Interesting.bob:
        return {"This is": testing}
    else:
        return {"poncalak": testing, "Message": "This is Poncalakkkk"}

#amra type hisebe path use korte pari jodi kono 1 ta directory by folder er address ke string hisebe store ba retrieve korte cai
# normally jodi string e abc/aa store korte cai sudhu abc store hobe / mane string ses
# Tai kono file er nested path soho entire path extract korte :path type use hoy
# Example: a/b/input.txt

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}  

#if the parameter is int,str,bool, etc it's a path or query parameter
#if it is a pydantic model it is always a request body

from logging import exception
from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Sonya@123"
app.config["MYSQL_DB"] = "userdetails"

mysql = MySQL(app)

@app.route("/students",methods=["GET"])
def students():
    result = {}
    try:
        temp_result = []
        cur = mysql.connection.cursor()
        cur.execute("select * from userdata")
        rows = cur.fetchall()
        
        for row in rows:
            temp_result.append({
                "id":row[0],
                "firstName":row[1],
                "lastName":row[2],
                "class":row[3],
                "department":row[4],
                "subject":row[5]
            })
           
    except Exception as e:
        print(e)
    finally:
        cur.close()
        
    return {"students":temp_result}, 200 , {"Content-Type":"text/json"}

@app.route("/student",methods=["POST","PUT"])
def student():
    
    try:
        cursor = mysql.connection.cursor()
        
        if request.method == "POST" :
            print("post method started...")
            content_type = request.headers.get("Content-Type")
            if content_type == 'application/json':
                
                payload = request.get_json()
                data = (        payload["id"],
                                payload["firstName"],
                                payload["lastName"],
                                payload["class"],
                                payload["department"],
                                payload["subject"])
                
                cursor.execute(f"""insert into 
                                userdata(id,student_first_name,student_last_name,class,department,subject) 
                                values (%s,%s,%s,%s,%s,%s)""",data)
                
                cursor.close()
                mysql.connection.commit()
                
                return {"message":"User inserted successfully."}, 201
            
        elif request.method == "PUT":
            print("put method started...")
            
            content_type = request.headers.get("Content-Type")
            if content_type == 'application/json':
                
                payload = request.get_json()
               
                data = (
                                    payload["firstName"],
                                    payload["lastName"],
                                    payload["class"],
                                    payload["department"],
                                    payload["subject"],
                                    payload["id"]
            
                                )
                print(data)
                cursor.execute("""UPDATE userdata SET
                                    student_first_name=%s,
                                    student_last_name=%s,
                                    class=%s,
                                    department=%s,
                                    subject=%s
                                    
                                    WHERE id=%s""", data )
                
                
                cursor.close()
                mysql.connection.commit()
                
                return {"message":"User updated successfully."}, 201
            
    except Exception as e:
        print(e)    
        
    return {"messgae":"Content type not supported."}, 400

@app.route("/student",methods=["DELETE"])
def delete_student():
    
    try:
        id = request.args.get("id")
        delete_flag = False
        
        cursor = mysql.connection.cursor()
        
        cursor.execute("select * from userdata")
        
        rows = cursor.fetchall()
        
        
        for row in rows:
            
            if int(id) == row[0]:
                cursor.execute("delete from userdata where id = %s",(id))
               
                delete_flag = True
        
        mysql.connection.commit()
        cursor.close()
        
        if delete_flag:
            return {"message": "user deleted successfully."}, 200
        else:
            return {"message": "No user found to be deleted."}, 200
        
    except Exception as e:
        print(e)
        return {"messgae":"Unexpected error occured."}, 500
    
if __name__ == "__main__":
    app.run(debug=True)
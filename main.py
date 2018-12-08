from flask import Flask, request, render_template
from flask_restful import reqparse, abort, Api, Resource
from pymongo import MongoClient


app = Flask(__name__)
api = Api(app)

#client = MongoClient('localhost', 27017)
client = MongoClient("mongodb://localhost:27017/")
todoDB = client["todoDB"]
todoCOL = todoDB["todo_list"]
todoCOL.drop() # clear todo collection

todolist   = [
  { "name": "todo1", "task": "build an API"},
  { "name": "todo2", "task": "?????"},
  { "name": "todo3", "task": "profit!"}
] # example data in list form

todoCOL.insert_many(todolist) # inserting example data

@app.route('/')
def home():
    return render_template('index.html')

parser = reqparse.RequestParser()
parser.add_argument('task')

# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):

    def delete(self, todo_id):
        #abort_if_todo_doesnt_exist(todo_id)
        for i in todoCOL.find():
            if i["name"]==todo_id:
                todoCOL.delete_one(i)
        return '', 204

# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return [i for i in todoCOL.find({},{ "_id": 0, "name": 1, "task": 1 })] # update the todo list

    def post(self):
        args = parser.parse_args()
        try:
            todo_id = len([i for i in todoCOL.find()]) + 1
            todo_id = 'todo%i' % todo_id
        except:
            todo_id = 'todo1'
        todo_id = len([i for i in todoCOL.find()]) + 1
        todo_id = 'todo%i' % todo_id
        inserted_value = todoCOL.insert_one({'name':todo_id,'task': args['task']})
        return {'name':todo_id,'task': args['task']}, 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


if __name__ == '__main__':
    app.run(debug=True)

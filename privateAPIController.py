from common import *
from datetime import datetime
import json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat(sep = " ")

        return json.JSONEncoder.default(self, o)

@app.route("/private-api/test", methods = ["POST"])
@login_required
def test():
    print(request.args.get("id"))
    print(json.loads(request.data))
    return request.data

#USER


@app.route("/private-api/user")
@login_required
def getUser():
    if request.method == "GET":
        uid = request.args.get("uid")
        username = request.args.get("username")
        email = request.args.get("email")

        if uid != None:
            user = ModelObject["userModel"].getUser(uid)
        elif username != None:
            user = ModelObject["userModel"].getUserByUsername(username)
        elif email != None:
            user = ModelObject["userModel"].getUserByEmail(email)
        else:
            return render_template("private-api/unknown-request.html")
        try:
            user.pop("password")
        except:
            print("password field cannot be popped!")
            return
        return json.dumps(user, cls=DateTimeEncoder)

    return redirect(url_for("index"))


@app.route("/private-api/current-user")
@login_required
def currentUser():
    return json.dumps(getCurrentUser(), cls=DateTimeEncoder)


@app.route("/private-api/is-there-this-username/<string:username>")
@login_required
def isThereThisUsername(username):
    data = dict()
    if ModelObject["userModel"].isThereThisUsername(username):
        data["result"] = True
    else:
        data["result"] = False
    
    return json.dumps(data)

@app.route("/private-api/is-there-this-email/<string:email>")
@login_required
def isThereThisEmail(email):
    data = dict()
    if ModelObject["userModel"].isThereThisEmail(email):
        data["result"] = True
    else:
        data["result"] = False
    
    return json.dumps(data)

@app.route("/private-api/user/is-global-admin/<string:uid>")
@login_required
def isGlobalAdmin(uid):
    data = dict()
    if ModelObject["userModel"].isGlobalAdmin(uid):
        data["result"] = True
    else:
        data["result"] = False
    
    return json.dumps(data)

@app.route("/private-api/follow/<string:uid>")
@login_required
def follow(uid):
    ModelObject["userModel"].follow(session["uid"], uid)

    return json.dumps({
        "result": "success"
    })

@app.route("/private-api/unfollow/<string:uid>")
@login_required
def unfollow(uid):
    ModelObject["userModel"].unfollow(session["uid"], uid)

    return json.dumps({
        "result": "success"
    })

@app.route("/private-api/user-links", methods = ["GET", "POST", "PUT", "DELETE"])
@login_required
def userLinks():
    if request.method == "GET":
        #Getting all user's links
        links = ModelObject["userModel"].getUserLinks(session["uid"])
        return json.dumps(links, cls=DateTimeEncoder)
    elif request.method == "POST":
        #Adding new user link
        data = json.loads(request.data)
        ModelObject["userModel"].addUserLink(session["uid"], data["name"], data["link"])
        return json.dumps({"result" : "success"})
        
    elif request.method == "PUT":
        #Updating a user link
        data = json.loads(request.data)
        ulid = request.args.get("ulid")
        link = ModelObject["userModel"].getUserLink(ulid)

        if link["uid"] == session["uid"]:
            ModelObject["userModel"].updateUserLink(ulid, data["name"], data["link"])
            return json.dumps({"result" : "success"})
        else:
            return render_template("private-api/forbidden-request.html")

    else:
        #Delete a user link
        #DELETE request

        ulid = request.args.get("ulid")
        link = ModelObject["userModel"].getUserLink(ulid)

        if link["uid"] == session["uid"]:
            ModelObject["userModel"].removeUserLink(ulid)
            return json.dumps({"result" : "success"})
        else:
            return render_template("private-api/forbidden-request.html")



#USER POSTS
@app.route("/private-api/user-posts", methods = ["GET", "POST", "PUT", "DELETE"])
@login_required
def userPosts():
    if request.method == "GET":
        #Get last posts
        uid = request.args.get("uid")
        upid = request.args.get("upid")
        
        if upid != None:
            posts = ModelObject["userPostModel"].getLastUserPosts(uid, 10, session["uid"])
        else:
            posts = ModelObject["userPostModel"].getNextUserPosts(uid, upid, 10, currentUser)
        
        return json.dumps(posts, cls=DateTimeEncoder)

    elif request.method == "POST":
        #Add user post
        data = json.loads(request.data)
        ModelObject["userPostModel"].addUserPost(session["uid"], data["post"])
        return json.dumps({"result" : "success"})

    elif request.method == "PUT":
        #Update user post
        data = json.loads(request.data)
        upid = request.args.get("upid")

        post = ModelObject["userPostModel"].getUserPost(upid)

        if post["uid"] == session["uid"]:
            ModelObject["userPostModel"].updateUserPost(data["upid"], data["post"])
            return json.dumps({"result" : "success"})
        else:
            return render_template("private-api/forbidden-request.html")

    else:
        #Delete a user post

        upid = request.args.get("upid")

        post = ModelObject["userPostModel"].getUserPost(upid)

        if post["uid"] == session["uid"]:
            ModelObject["userPostModel"].removeUserPost(upid)
            return '{"result" : "success"}'
        else:
            return render_template("private-api/forbidden-request.html")

@app.route("/private-api/next-following-posts")
@login_required
def getNextFollowingPosts():
    if request.method == "GET":
        upid = request.args.get("upid")
        
        if upid != None:
            posts = ModelObject["userPostModel"].getNextFollowingPosts(session["uid"], upid)
            return json.dumps(posts, cls=DateTimeEncoder)
    
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/new-following-post-number")
@login_required
def getNewFollowingPostNumber():
    if request.method == "GET":
        upid = request.args.get("upid")
        if upid != None:
            number = ModelObject["userPostModel"].getNewFollowingPostNumber(session["uid"], upid)

            return json.dumps({
                "number" : number
            })
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/new-following-posts")
@login_required
def getNewFollowingPosts():
    if request.method == "GET":
        upid = request.args.get("upid")

        if upid != None:
            posts = ModelObject["userPostModel"].getNewFollowingPosts(session["uid"], upid)
            return json.dumps(posts, cls=DateTimeEncoder)

    return render_template("private-api/unknown-request.html")

@app.route("/private-api/user-posts/<string:upid>/like")
@login_required
def likeUserPost(upid):

    ModelObject["userPostModel"].likeUserPost(session["uid"], upid)
    return json.dumps({"result" : "success"})


@app.route("/private-api/user-posts/<string:upid>/unlike")
@login_required
def unlikeUserPost(upid):

    ModelObject["userPostModel"].unlikeUserPost(session["uid"], upid)
    return json.dumps({"result" : "success"})

@app.route("/private-api/user-posts/<string:upid>/likes/number")
@login_required
def userPostLikeNumber(upid):
    number = ModelObject["userPostModel"].getUserPostLikeNumber(upid)
    return json.dumps({"number" : number})


@app.route("/private-api/user-posts/<string:upid>/comments/number")
@login_required
def userPostCommentNumber(upid):
    number = ModelObject["userPostModel"].getUserPostCommentNumber(upid)
    return json.dumps({"number" : number})




@app.route("/private-api/user-posts/<string:upid>/comments", methods = ["GET", "POST", "PUT", "DELETE"])
@login_required
def userPostComments(upid):
    if request.method == "GET":
        #Get last post comments
        upcid = request.args.get("upcid")
        number = request.args.get("number")

        try:
            number = int(number)
        except:
            number = 2

        if upcid == None:
            comments = ModelObject["userPostModel"].getLastUserPostComments(upid, number, session["uid"])
        else:
            comments = ModelObject["userPostModel"].getPreviousUserPostComments(upid, upcid, number, session["uid"])
            print(comments)
        return json.dumps(comments, cls=DateTimeEncoder)

    elif request.method == "POST":
        #Add a new user post comment
        data = json.loads(request.data)
        ModelObject["userPostModel"].addUserPostComment(session["uid"], upid, data["comment"])

        return json.dumps({"result" : "success"})
    elif request.method == "PUT":
        #Update user post comment
        upcid = request.args.get("upcid")
        data = json.loads(request.data)
        comment = ModelObject["userPostModel"].getUserPostComment(upcid)

        if comment["uid"] == session["uid"]:
            ModelObject["userPostModel"].updateUserPostComment(upcid, data["comment"])
            return json.dumps({"result" : "success"})
        
        return render_template("private-api/forbidden-request.html")

    else:
        #Delete a user post comment
        upcid = request.args.get("upcid")
        comment = ModelObject["userPostModel"].getUserPostComment(upcid)

        if comment["uid"] == session["uid"]:
            ModelObject["userPostModel"].removeUserPostComment(upcid)
            return '{"result" : "success"}'
        
        return render_template("private-api/forbidden-request.html")

    return render_template("private-api/unknown-request.html")


@app.route("/private-api/user-posts/comments/<string:upcid>/like")
@login_required
def likeUserPostComment(upcid):
    ModelObject["userPostModel"].likeUserPostComment(session["uid"], upcid)
    return '{"result" : "success"}'


@app.route("/private-api/user-posts/comments/<string:upcid>/unlike")
@login_required
def unlikeUserPostComment(upcid):
    ModelObject["userPostModel"].unlikeUserPostComment(session["uid"], upcid)
    return '{"result" : "success"}'

@app.route("/private-api/user-posts/comments/<string:upcid>/like-number")
@login_required
def userPostCommentLikeNumber(upcid):
    number = ModelObject["userPostModel"].getUserPostCommentLikeNumber(upcid)
    return json.dumps({"number" : number})



#USER SKILLS
@app.route("/private-api/user-skills", methods = ["GET", "POST", "DELETE"])
@login_required
def userSkills():
    if request.method == "GET":
        uid = request.args.get("uid")

        if uid == None:
            uid == session["uid"]
        
        skills = ModelObject["skillModel"].getUserSkills(uid)

        return json.dumps(skills, cls=DateTimeEncoder)

    elif request.method == "POST":
        skill = request.args.get("skill")
        if skill != None:
            ModelObject["skillModel"].addUserSkill(session["uid"], skill)
            return '{"result" : "success"}'

    else:
        #Delete a user skill
        skid = request.args.get("skid")

        if skid != None:
            skill = ModelObject["skillModel"].getUserSkill(skid)

            if skill["uid"] == session["uid"]:
                ModelObject["skillModel"].removeUserSkill(skid)
                return '{"result" : "success"}'
            else:
                return render_template("private-api/forbidden-request.html")
        
    return render_template("private-api/unknown-request.html")

#SEATER SKILLS
@app.route("/private-api/seater-skills", methods = ["GET", "POST", "DELETE"])
@login_required
def seaterSkills():
    if request.method == "GET":
        #Get seater skills
        sid = request.args.get("sid")

        if sid != None:
            skills = ModelObject["skillModel"].getUserSkills(uid)
            return json.dumps(skills, cls=DateTimeEncoder)
        return render_template("private-api/unknown-request.html")

    elif request.method == "POST":
        #Add seater skill
        sid = request.args.get("sid")
        skill = request.args.get("skill")

        pid = ModelObject["seaterModel"].getSeater(sid)["pid"]

        if ModelObject["projectModel"].isProjectAdmin(session["uid"], pid):
            if skill != None:
                ModelObject["skillModel"].addSeaterSkill(sid, skill)
                return '{"result" : "success"}'

    else:
        #Delete a user skill
        skid = request.args.get("skid")

        if skid != None:
            skill = ModelObject["skillModel"].getUserSkill(skid)

            if skill["uid"] == session["uid"]:
                ModelObject["skillModel"].removeUserSkill(skid)
                return '{"result" : "success"}'
            else:
                return render_template("private-api/forbidden-request.html")
        
    return render_template("private-api/unknown-request.html")


#SEATERS
@app.route("/private-api/projects/<string:pid>/seaters/all")
@login_required
def projectSeaters(pid):
    seaters = ModelObject["seaterModel"].getAllProjectSeaters(pid)

    return json.dumps(seaters, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/seaters/empty")
@login_required
def projectEmptySeaters(pid):
    seaters = ModelObject["seaterModel"].getEmptyProjectSeaters(pid)

    return json.dumps(seaters, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/seaters/filled")
@login_required
def projectFilledSeaters(pid):
    seaters = ModelObject["seaterModel"].getFilledProjectSeaters(pid)

    return json.dumps(seaters, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/seaters/number")
@login_required
def projectEmptySeaterNumber(pid):
    number = ModelObject["seaterModel"].getEmptyProjectSeaterNumber(pid)

    return json.dumps({"number" : number})

@app.route("/private-api/users/<string:uid>/seaters")
@login_required
def userSeaters(uid):
    seaters = ModelObject["seaterModel"].getUserSeaters(uid)
    return json.dumps(seaters, cls=DateTimeEncoder)

@app.route("/private-api/users/<string:uid>/seaters/number")
@login_required
def userSeaterNumber(uid):
    number = ModelObject["seaterModel"].getUserSeaterNumber(uid)
    return json.dumps({"number" : number})

@app.route("/private-api/seaters/<string:sid>")
@login_required
def getSeater(sid):
    seater = ModelObject["seaterModel"].getSeater(sid)
    return json.dumps(seater, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/seaters", methods = ["POST"])
@login_required
def createSeater(pid):
    print("1")
    if ModelObject["projectModel"].isProjectAdmin(session["uid"], pid):
        seater = json.loads(request.data)
        seater["pid"] = pid
        ModelObject["seaterModel"].createSeater(pid, seater)

        return '{"result" : "success"}'
    return render_template("private-api/forbidden-request.html")

@app.route("/private-api/seaters/<string:sid>", methods = ["DELETE"])
@login_required
def removeSeater(sid):
    seater = ModelObject["seaterModel"].getSeater(sid)
    if seater != None:
        if ModelObject["projectModel"].isProjectAdmin(session["uid"], seater["pid"]):
            ModelObject["seaterModel"].removeSeater(sid)
            return '{"result" : "success"}'
        else:
            return render_template("private-api/forbidden-request.html")
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/seaters/<string:sid>/dismiss-user")
@login_required
def dismissUser(sid):
    seater = ModelObject["seaterModel"].getSeater(sid)

    if seater != None:
        if ModelObject["projectModel"].isProjectAdmin(session["uid"], seater["pid"]):
            ModelObject["seaterModel"].dismissUser(sid)
            return '{"result" : "success"}'
        else:
            return render_template("private-api/forbidden-request.html")
    
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/seaters/<string:sid>", methods = ["PUT"])
@login_required
def updateSeater(sid):
    seater = ModelObject["seaterModel"].getSeater(sid)

    if seater != None:
        if ModelObject["projectModel"].isProjectAdmin(session["uid"], seater["pid"]):
            seater = json.loads(request.data)
            ModelObject["seaterModel"].updateSeater(sid, seater["title"], seater["description"])
            return '{"result" : "success"}'
        else:
            return render_template("private-api/forbidden-request.html")
    
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/seaters/<string:sid>/assign/<string:uid>")
@login_required
def assignUser(sid, uid):
    seater = ModelObject["seaterModel"].getSeater(sid)

    if seater != None:
        if ModelObject["projectModel"].isProjectAdmin(session["uid"], seater["pid"]):
            if ModelObject["seaterModel"].isThereSeaterAspiration(uid, sid):
                ModelObject["seaterModel"].assignUser(uid, sid)
                return '{"result" : "success"}'
        else:
            return render_template("private-api/forbidden-request.html")
    
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/seaters/<string:sid>/assign/<string:uid>")
@login_required
def unassignUser(sid, uid):
    seater = ModelObject["seaterModel"].getSeater(sid)

    if seater != None:
        if ModelObject["projectModel"].isProjectAdmin(session["uid"], seater["pid"]):
            ModelObject["seaterModel"].unassignUser(sid)
            return '{"result" : "success"}'
        else:
            return render_template("private-api/forbidden-request.html")
    
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/seaters/<string:sid>/aspire")
@login_required
def aspireSeater(sid):
    ModelObject["seaterModel"].aspireSeater(session["uid"], sid)
    return '{"result" : "success"}'

@app.route("/private-api/seaters/<string:sid>/cancel-aspiration")
@login_required
def cancelSeaterAspiration(sid):
    if ModelObject["seaterModel"].isThereSeaterAspiration(session["uid"], sid):
        ModelObject["seaterModel"].cancelSeaterAspiration(session["uid"], sid)
        return '{"result" : "success"}'
    else:
        return render_template("private-api/forbidden-request.html")

@app.route("/private-api/projects/<string:pid>/seater-aspirations")
@login_required
def seaterAspirations(pid):
    if ModelObject["projectModel"].isProjectAdmin(session["uid"], pid):
        aspirations = ModelObject["seaterModel"].getSeaterAspirations(pid)
        return json.dumps(aspirations, cls=DateTimeEncoder)
    return render_template("private-api/forbidden-request.html")

@app.route("/private-api/seaters/<string:sid>/reject")
@login_required
def rejectSeater(sid):
    seater = ModelObject["seaterModel"].getSeater(sid)
    uid = request.args.get("uid")

    if seater != None and uid != None:
        if ModelObject["projectModel"].isProjectAdmin(session["uid"], seater["pid"]):
            ModelObject["seaterModel"].rejectSeaterAspiration(uid, sid)
            return '{"result" : "success"}'
        else:
            return render_template("private-api/forbidden-request.html")
    
    return render_template("private-api/unknown-request.html")


#PROJECT CONTROLLER
@app.route("/private-api/user/<string:uid>/projects")
@login_required
def getUserProjects(uid):
    projects = ModelObject["projectModel"].getUserProjects(uid)

    return json.dumps(projects, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>")
@login_required
def getProject(pid):
    project = ModelObject["projectModel"].getProject(pid)

    return json.dumps(project, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/members")
@login_required
def getProjectMembers(pid):
    members = ModelObject["projectModel"].getMembers(pid)

    return json.dumps(members, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/members/number")
def getNumberOfMembers(pid):
    number = ModelObject["projectModel"].getNumberOfMembers(pid)

    return json.dumps({"number" : number})

@app.route("/private-api/popular-projects/")
@login_required
def getPopularProjects():
    howMany = request.args.get("how-many")

    if howMany == None:
        howMany = 4

    projects = ModelObject["projectModel"].getPopularProjects(howMany)
    
    return json.dumps(projects, cls=DateTimeEncoder)

@app.route("/private-api/check-project-name/<string:name>")
@login_required
def isThereThisProjectName(name):
    result = ModelObject["projectModel"].isThereThisProjectName(name)

    return json.dumps({
        "result": result
    })
    

@app.route("/private-api/projects/<string:pid>/photo", methods = ["PUT", "DELETE"])
@login_required
def projectPhoto(pid):
    if not ModelObject["projectModel"].isProjectAdmin(session["uid"], pid):
        return render_template("private-api/forbidden-request.html")

    if request.method == "PUT":
        # check if the post request has the file part
        if 'photo' not in request.files:
            return '{result : "fail"}'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return json.dumps({
                "result" : "fail",
                "msg" : "Please choose a photo"
            })
        if file and isAnAllowedPhotoFile(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER + "/projects/pp", filename))
            ModelObject["projectModel"].updateProjectPhoto(pid, filename)
            return '{"result" : "success"}'
    else:
        #Delete Project Photo
        ModelObject["projectModel"].updateProjectPhoto(pid, NULL)
        return '{"result" : "success"}'

@app.route("/private-api/projects/<string:pid>/name/<string:newName>", methods = ["PUT"])
@login_required
def updateProjectName(pid, newName):
    if not ModelObject["projectModel"].isProjectAdmin(session["uid"], pid):
        return render_template("private-api/forbidden-request.html")

    if not isValidProjectName(newName):
        return json.dumps({
            "result" : "fail",
            "msg" : "Project name is not valid"
        })
    
    ModelObject["projectModel"].updateProjectName(pid, newName)
    return '{"result" : "success"}'

@app.route("/private-api/projects/<string:pid>/short-description", methods = ["PUT"])
@login_required
def updateProjectShortDescription(pid):
    if not ModelObject["projectModel"].isProjectAdmin(session["uid"], pid):
        return render_template("private-api/forbidden-request.html")
    
    description = json.loads(request.data)["description"]

    ModelObject["projectModel"].updateShortDescription(pid, description)
    return '{"result" : "success"}'

@app.route("/private-api/projects/<string:pid>/full-description", methods = ["PUT"])
@login_required
def updateProjectFullDescription(pid):
    if not ModelObject["projectModel"].isProjectAdmin(session["uid"], pid):
        return render_template("private-api/forbidden-request.html")
    
    description = json.loads(request.data)["description"]

    ModelObject["projectModel"].updateFullDescription(pid, description)
    return '{"result" : "success"}'

@app.route("/private-api/projects/<string:pid>/admins")
@login_required
def getProjectAdmins(pid):
    admins = ModelObject["projectModel"].getProjectAdmins(pid)
    return json.dumps(admins, cls=DateTimeEncoder)



#PROJECT POST CONTROLLER


@app.route("/private-api/projects/<string:pid>/posts", methods = ["GET", "POST", "PUT", "DELETE"])
@login_required
def projectPosts(pid):
    if request.method == "GET":
        #Get last posts
        ppid = request.args.get("ppid")
        if ppid == None:
            ModelObject["projectPostModel"].getLastPosts(pid, 10, session["uid"])
        else:
            ModelObject["projectPostModel"].getNextPosts(pid, ppid, 10, currentUser)

        return json.dumps(posts, cls=DateTimeEncoder)

    elif request.method == "POST":
        if not ModelObject["projectModel"].isProjectMember(session["uid"], pid):
            return render_template("private-api/forbidden-request.html")

        #Add project post
        data = json.loads(request.data)
        ModelObject["projectPostModel"].addPost(session["uid"], pid, data["post"])
        return json.dumps({"result" : "success"})

    elif request.method == "PUT":
        if not ModelObject["projectModel"].isProjectMember(session["uid"], pid):
            return render_template("private-api/forbidden-request.html")

        #Update project post
        data = json.loads(request.data)
        ppid = request.args.get("ppid")

        post = ModelObject["projectPostModel"].getProjectPost(ppid)

        if post["uid"] == session["uid"]:
            ModelObject["projectPostModel"].updateProjectPost(data["ppid"], data["post"])
            return json.dumps({"result" : "success"})
        else:
            return render_template("private-api/forbidden-request.html")

    else:
        #Delete a user post

        ppid = request.args.get("ppid")

        post = ModelObject["projectPostModel"].getProjectPost(ppid)

        if post["uid"] == session["uid"]:
            ModelObject["userModel"].removeUserPost(ppid)
            return '{"result" : "success"}'
        else:
            return render_template("private-api/forbidden-request.html")

@app.route("/private-api/project-posts/<string:ppid>/like")
@login_required
def likeProjectPost(ppid):
    ModelObject["projectPostModel"].likeProjectPost(session["uid"], ppid)
    return json.dumps({"result" : "success"})


@app.route("/private-api/project-posts/<string:ppid>/unlike")
@login_required
def unlikeProjectPost(ppid):
    ModelObject["projectPostModel"].unlikeProjectPost(session["uid"], upid)
    return json.dumps({"result" : "success"})

@app.route("/private-api/project-posts/<string:ppid>/like-number")
@login_required
def projectPostLikeNumber(ppid):
    number = ModelObject["projectPostModel"].getProjectPostLikeNumber(ppid)
    return json.dumps({"number" : number})


@app.route("/private-api/project-posts/<string:ppid>/comments", methods = ["GET", "POST", "PUT", "DELETE"])
@login_required
def projectPostComments(ppid):
    if request.method == "GET":
        #Get last post comments
        ppcid = request.args.get("ppcid")
        if ppcid == None:
            comments = ModelObject["projectPostModel"].getLastProjectPostComments(ppid, 5, session["uid"])
        else:
            comments = ModelObject["projectPostModel"].getNextProjectPostComments(ppid, ppcid, 5, session["uid"])
        return json.dumps(comments, cls=DateTimeEncoder)
    elif request.method == "POST":
        #Add a new user post comment
        data = json.loads(request.data)
        ModelObject["projectPostModel"].addProjectPostComment(session["uid"], ppid, data["comment"])

        return json.dumps({"result" : "success"})
    elif request.method == "PUT":
        #Update user post comment
        data = json.loads(request.data)
        ppcid = request.args.get("ppcid")
        comment = ModelObject["projectPostModel"].getProjectPostComment(ppcid)

        if comment["uid"] == session["uid"]:
            ModelObject["projectPostModel"].updateProjectPostComment(ppcid, data["comment"])
            return json.dumps({"result" : "success"})
        
        return render_template("private-api/forbidden-request.html")

    else:
        #Delete a user post comment
        ppcid = request.args.get("ppcid")
        comment = ModelObject["projectPostModel"].getProjectPostComment(ppcid)

        if comment["uid"] == session["uid"]:
            ModelObject["userPostModel"].removeProjectPostComment(ppcid)
            return '{"result" : "success"}'
        
        return render_template("private-api/forbidden-request.html")

    return render_template("private-api/unknown-request.html")


@app.route("/private-api/project-posts/comments/<string:ppcid>/like")
@login_required
def likeProjectPostComment(ppcid):
    ModelObject["projectPostModel"].likeProjectPostComment(session["uid"], ppcid)
    return '{"result" : "success"}'


@app.route("/private-api/project-posts/comments/<string:ppcid>/unlike")
@login_required
def unlikeProjectPostComment(upcid):
    ModelObject["projectPostModel"].unlikeProjectPostComment(session["uid"], ppcid)
    return '{"result" : "success"}'

@app.route("/private-api/project-posts/comments/<string:ppcid>/like-number")
@login_required
def projectPostCommentLikeNumber(upcid):
    number = ModelObject["projectPostModel"].getProjectPostCommentLikeNumber(ppcid)
    return json.dumps({"number": number})



#NOTIFICATION CONTROLLER

@app.route("/private-api/notifications/new")
@login_required
def getNewNotifications():
    notifications = ModelObject["notificationModel"].getNewNotifications(session["uid"], 10)
    return json.dumps(notifications, cls=DateTimeEncoder)

@app.route("/private-api/notifications/new/number")
@login_required
def getNewNotificationNumber():
    number = ModelObject["notificationModel"].getNewNotificationNumber(session["uid"])
    return json.dumps({
        "number" : number
    })


@app.route("/private-api/notifications/last")
@login_required
def getLastNotifications():
    notifications = ModelObject["notificationModel"].getNotifications(session["uid"], 20)
    return json.dumps(notifications, cls=DateTimeEncoder)


#MESSAGE CONTROLLER
@app.route("/private-api/messages/send")
@login_required
def sendMessage():
    message = json.loads(request.data)
    ModelObject["messageModel"].sendMessage(session["uid"], message["receiver_id"], message["text"])
    return '{"result" : "success"}'

@app.route("/private-api/messages/delete/<string:mid>")
@login_required
def deleteMessage(mid):
    if not ModelObject["messageModel"].isTheUserMessageOwner(session["uid"], mid):
        return render_template("private-api/forbidden-request.html")

    ModelObject["messageModel"].deleteMessage(session["uid"], mid)
    return '{"result" : "success"}'

@app.route("/private-api/messages/new-dialog-number")
@login_required
def newDialogNumber():
    number = ModelObject["messageModel"].getNewMessageDialogNumber(session["uid"])
    return json.dumps({
        "number" : number
    })

@app.route("/private-api/messages/dialogs")
@login_required
def getDialogList():
    dialogList = ModelObject["messageModel"].getDialogList(session["uid"])

    return json.dumps({
        "dialogList" : dialogList
    }, cls=DateTimeEncoder)


@app.route("/private-api/messages/dialogs/<string:uid>")
@login_required
def getDialog(uid):
    page = request.args.get("page")

    if page == None:
        page = 1
    
    msgList = ModelObject["messageModel"].getDialog(session["uid"], uid, page, 10)

    return json.dumps({
        "msgList" : msgList
    }, cls=DateTimeEncoder)



#SEARCH CONTROLLER
@app.route("/private-api/q/<string:query>")
def generalSearch(query):
    userResults = ModelObject["userModel"].searchUsers(query, 5)
    projectResults = ModelObject["projectModel"].searchProjects(query, 5)

    return json.dumps({
        "userResults" : userResults,
        "projectResults" : projectResults
    }, cls=DateTimeEncoder)

@app.route("/private-api/q/skills/<string:query>")
@login_required
def skillSearch(query):
    skills = ModelObject["skillModel"].searchSkills(query, 5)

    return json.dumps(skills, cls=DateTimeEncoder)
from project.lib.database import Database

class SkillModel():
  
  @staticmethod
  def getUserSkills(uid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT * FROM userSkills
      INNER JOIN skills ON skills.skid = userSkills.skid WHERE uid = %s"""
      result = cursor.execute(query, (uid,) )
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  @staticmethod
  def getUserSkill(skid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT * FROM userSkills
      INNER JOIN skills ON skills.skid = userSkills.skid WHERE skid = %s"""
      result = cursor.execute(query, (skid,) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def getSeaterSkill(skid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT * FROM seaterSkills
      INNER JOIN skills ON skills.skid = seaterSkills.skid WHERE skid = %s"""
      result = cursor.execute(query, (skid,) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def getSeaterSkills(sid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT * FROM seaterSkills
      INNER JOIN skills ON skills.skid = seaterSkills.skid WHERE sid = %s"""
      result = cursor.execute(query, (sid,) )
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  @staticmethod
  def getSkillByName(name):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM skills WHERE name = %s"
      result = cursor.execute(query, (name,) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def addUserSkill(uid, skill):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)

    try:
      if SkillModel.isThereThisSkill(skill):
        skid = SkillModel.getSkillByName(skill)["skid"]
      
      else:
        #Adding skill to the skills table
        query = "INSERT INTO skills(name) VALUES(%s)"
        cursor.execute(query, (skill,) )
        
        #Getting new added skill id
        skid = cursor.lastrowid

      #Adding user skill
      query = "INSERT INTO userSkills(uid, skid) VALUES(%s, %s)"
      cursor.execute(query, (uid, skid) )

      connection.commit()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return skid

  @staticmethod
  def addSeaterSkill(sid, skill):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)

    try:
      if SkillModel.isThereThisSkill(skill):
        skid = SkillModel.getSkillByName(skill)["skid"]
      
      else:
        #Adding skill to the skills table
        query = "INSERT INTO skills(name) VALUES(%s)"
        cursor.execute(query, (skill,) )
        
        #Getting new added skill id
        skid = cursor.lastrowid

      #Adding seater skill
      query = "INSERT INTO seaterSkills(sid, skid) VALUES(%s, %s)"
      cursor.execute(query, (sid, skid) )

      connection.commit()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return skid

  @staticmethod
  def removeUserSkill(uid, skid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM userSkills WHERE uid = %s AND skid = %s"
      cursor.execute(query, (uid, skid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  @staticmethod
  def removeSeaterSkill(sid, skillName):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """DELETE FROM seaterSkills WHERE sid = %s AND skid = 
                (SELECT skid FROM skills WHERE name = %s)"""
      cursor.execute(query, (sid, skillName) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  @staticmethod
  def searchSkills(keyword, number):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM skills WHERE name LIKE %s LIMIT %s"
      result = cursor.execute(query, ("%" + keyword + "%", number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def isThereThisSkill(skillName):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM skills WHERE name = %s"
      result = cursor.execute(query, (skillName,) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return (result != None)
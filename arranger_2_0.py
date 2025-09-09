# -*- coding: utf-8 -*-
# Copyright Xinyuan Zhou 2024

import sys
def myexcepthook(type, value, traceback, oldhook=sys.excepthook):
    oldhook(type, value, traceback)
    input("Press RETURN to exit. ")
sys.excepthook = myexcepthook
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
os.chdir(parent_dir)
import io
import csv
def read_people(csv_content):
    data_list = []
    with io.StringIO(csv_content) as file:
        reader = csv.reader(file, dialect='excel')
        next(reader)
        for row in reader:
            if len(row) >= 4:
                item = (row[0], row[1], int(row[2]), row[3])  # (str, str, int, str)
                data_list.append(item)
            else:
              raise ValueError("Row without at least 4 values")
    return data_list
def read_requests(csv_content):
    data_list = []
    with io.StringIO(csv_content) as file:
        reader = csv.reader(file, dialect='excel')
        next(reader)  # Skip the first row
        for row in reader:
            # Ensure there are at least 4 items; if not, use None for the fifth
            if len(row) >= 4:
                first_tuple = (row[0], int(row[1]))  # (firststr, secondint)
                second_tuple = (row[2], int(row[3]))  # (thirdstr, fourthint)
                fifth_int = int(row[4]) if len(row) > 4 and not row[4] == '' else None
                item = (first_tuple, second_tuple, fifth_int)
                data_list.append(item)
            else:
              raise ValueError("Row without at least 4 values")
    return data_list
def read_antirequests(csv_content):
    data_list = []
    with io.StringIO(csv_content) as file:
        reader = csv.reader(file, dialect='excel')
        next(reader)  # Skip the first row
        for row in reader:
            if len(row) >= 4:
                first_tuple = (row[0], int(row[1]))  # (firststr, secondint)
                second_tuple = (row[2], int(row[3]))  # (thirdstr, fourthint)
                data_list.append((first_tuple, second_tuple))
            else:
              raise ValueError("Row without at least 4 values")
    return data_list
def read_rooms(csv_content):
    data_list = []
    with io.StringIO(csv_content) as file:
        reader = csv.reader(file, dialect='excel')
        next(reader)  # Skip the first row
        for row in reader:
            data_list.append(row[0])
    return data_list
print("Reading Student Info... from student_info.csv")
f = open('student_info.csv', 'rb')
studentscsv = f.read()
f.close()
print("Reading Requests... from requests.csv")
f = open('requests.csv', 'rb')
requestscsv = f.read()
f.close()
print("Reading anti-Requests... from antirequests.csv")
f = open('antirequests.csv', 'rb')
antirequestscsv = f.read()
f.close()
studentdata = read_people(studentscsv.decode())
requestsdata = read_requests(requestscsv.decode())
antirequestsdata = read_antirequests(antirequestscsv.decode())
print("Reading room numbers... from roomnums.csv")
f = open('roomnums.csv', 'rb')
roomcsv = f.read()
f.close()
roomnums = read_rooms(roomcsv.decode())
limb = int(input("ENTER DATA - Multiple-grade-level pool: Limits for boys = "))
limg = int(input("ENTER DATA - Multiple-grade-level pool: Limits for girls = "))
limits_multiple = {"Boy": limb, "Girl": limg}
m = int(input("ENTER DATA - # of people in each room = "))
"""
The SCIP Optimization Suite 9.0. Suresh Bolusani, Mathieu Besançon, Ksenia Bestuzheva, Antonia Chmiela, João Dionísio, Tim Donkiewicz, Jasper van Doornmalen, Leon Eifler, Mohammed Ghannam, Ambros Gleixner, Christoph Graczyk, Katrin Halbig, Ivo Hedtke, Alexander Hoen, Christopher Hojny, Rolf van der Hulst, Dominik Kamp, Thorsten Koch, Kevin Kofler, Jurgen Lentz, Julian Manns, Gioni Mexi, Erik Mühmer, Marc E. Pfetsch, Franziska Schlösser, Felipe Serrano, Yuji Shinano, Mark Turner, Stefan Vigerske, Dieter Weninger, Lixing Xu. Available at Optimization Online and as ZIB-Report 24-02-29, February 2024
Bynum, Michael L., Gabriel A. Hackebeil, William E. Hart, Carl D. Laird, Bethany L. Nicholson, John D. Siirola, Jean-Paul Watson, and David L. Woodruff. Pyomo - Optimization Modeling in Python. Third Edition Vol. 67. Springer, 2021.
Hart, William E., Jean-Paul Watson, and David L. Woodruff. "Pyomo: modeling and solving mathematical programs in Python." Mathematical Programming Computation 3(3) (2011): 219-260.
"""
from pyomo.environ import *
import math
def solve(n,m,requests,antirequests):
  k = math.ceil(n/m)
  model = ConcreteModel()
  model.people = RangeSet(0, n-1)
  model.rooms = RangeSet(0, k-1)
  model.requests = Set(initialize=requests, dimen=2)
  model.antirequests = Set(initialize=antirequests, dimen=2)
  model.x = Var(model.people, model.rooms, domain=Binary)
  model.y1 = Var(model.requests, model.rooms, domain=Binary)
  model.y2 = Var(model.antirequests, model.rooms, domain=Binary)
  def requests_together_rule(model, p, q, j):
    return 2 * model.y1[p, q, j] <= model.x[p, j] + model.x[q, j]
  model.requests_together = Constraint(model.requests, model.rooms, rule=requests_together_rule)
  def antirequests_together_rule(model, p, q, j):
    return 2 * model.y2[p, q, j] <= model.x[p, j] + model.x[q, j]
  model.antirequests_together = Constraint(model.antirequests, model.rooms, rule=antirequests_together_rule)
  def objective_function(model):
      return (sum(sum(model.y1[p, q, j] for j in model.rooms) for (p, q) in model.requests)
            + len(antirequests)
            - sum(sum(model.y2[p, q, j] for j in model.rooms) for (p, q) in model.antirequests))
  model.obj = Objective(rule=objective_function, sense=maximize)
  def person_assigned_rule(model, i):
      return sum(model.x[i, j] for j in model.rooms) == 1
  model.person_assigned = Constraint(model.people, rule=person_assigned_rule)
  def room_capacity_rule(model, j):
      if j != k - 1 or n % m == 0:
        return sum(model.x[i, j] for i in model.people) == m
      else:
        return sum(model.x[i, j] for i in model.people) == (n % m)
  model.room_capacity = Constraint(model.rooms, rule=room_capacity_rule)
  solver = SolverFactory('cbc', executable='program/cbc.exe')
  solver.options['seconds'] = 180
  result = solver.solve(model, tee=True)
  ret = {}
  for i in range(n):
    for j in range(k):
      if int(model.x[i, j]()+0.01) == 1:
        if j not in ret:
          ret[j] = []
        ret[j].append(i)
  print(f"Satisfied, {int(value(model.obj))}")
  return ret

class Student:
  def __repr__(self):
    return f"--student-- {self.lastname} {self.firstname} Grade {self.grade} {self.gender} object id {id(self)%10000}"
  def __str__(self):
    return self.__repr__()
  def __init__(self, lastname, firstname, grade, gender):
    self.lastname = lastname
    self.firstname = firstname
    self.grade = grade
    self.gender = gender
    self.multirequests = False
class Request:
  def __repr__(self):
    return f"request between {self.person1} AND {self.person2}"
  def __str__(self):
    return self.__repr__()
  def __init__(self, person1, person2):
    self.person1 = person1
    self.person2 = person2
class AntiRequest:
  def __repr__(self):
    return f"anti-request between {self.person1} AND {self.person2}"
  def __str__(self):
    return self.__repr__()
  def __init__(self, person1, person2):
    self.person1 = person1
    self.person2 = person2
students = []
studentid = -1
for (last, first, grade, gend) in studentdata:
  studentid += 1
  stu = Student(last, first, grade, gend)
  stu.id = studentid
  students.append(stu)
requests = []
request_pool = {"Boy": [], "Girl": []}
for ((name1, grade1), (name2, grade2), priority) in requestsdata:
  ref1, ref2 = None, None
  for student in students:
    if student.firstname + " " + student.lastname == name1 and student.grade == grade1:
      ref1 = student
    if student.firstname + " " + student.lastname == name2 and student.grade == grade2:
      ref2 = student
  print("request", ((name1, grade1), (name2, grade2)), '\n ', ref1, '\n ', ref2)
  # Are they both boys or both girls?
  if ref1.gender != ref2.gender:
    # Nope!
    print("      INVALID")
    continue
  # Are they in the same grade level?
  if ref1.grade != ref2.grade:
    # OK, so let's put it into the pool
    req = Request(ref1, ref2)
    req.priority = priority # does not apply to all requests
    request_pool[ref1.gender].append(req) # we know gender are same by this point
    print("      QUEUED")
    continue # let's not put it in the main requests yet.
  requests.append(Request(ref1, ref2))
# Next we sort the requests by sector.
sectors = ("Boy6", "Boy7", "Boy8", "BoyM", "Girl6", "Girl7", "Girl8", "GirlM")
requests_by_sector = {}
students_by_sector = {}
antirequests_by_sector = {}
for sector_name in sectors:
  requests_by_sector[sector_name] = []
  antirequests_by_sector[sector_name] = []
  students_by_sector[sector_name] = []
def key_priority(a):
  return a.priority

# Handle multi-grade-lvl
for gender in request_pool:
  lst = request_pool[gender]
  lst = sorted(lst, key=key_priority)
  ppl = set()
  for r in lst:
    new = 2 - (r.person1 in ppl) - (r.person2 in ppl)
    if len(ppl) + new <= limits_multiple[gender]:
      ppl.add(r.person1)
      ppl.add(r.person2)
      r.person1.multirequests = True
      r.person2.multirequests = True
      requests_by_sector[gender + "M"].append(r)
  for p in ppl:
    students_by_sector[gender + "M"].append(p)
    p.sector = gender + "M"
  # print(requests_by_sector[gender + "M"], students_by_sector[gender + "M"])
for request in requests:
  if not (request.person1.multirequests or request.person2.multirequests):
    requests_by_sector[request.person1.gender + str(request.person1.grade)].append(request)
for student in students:
  if not student.multirequests:
    students_by_sector[student.gender + str(student.grade)].append(student)
    student.sector = student.gender + str(student.grade)

# Read and handle anti-requests
for ((name1, grade1), (name2, grade2)) in antirequestsdata:
  ref1, ref2 = None, None
  for student in students:
    if student.firstname + " " + student.lastname == name1 and student.grade == grade1:
      ref1 = student
    if student.firstname + " " + student.lastname == name2 and student.grade == grade2:
      ref2 = student
  if ref1.sector == ref2.sector:
    antirequests_by_sector[ref1.sector].append(AntiRequest(ref1, ref2))

"""Solve sectors. Push extras into leftovers."""

def anonymize(sector):
  students = students_by_sector[sector]
  requests = requests_by_sector[sector]
  antirequests = antirequests_by_sector[sector]
  mp = {value: key for (key, value) in enumerate(students)}
  request_anoy = []
  for request in requests:
    request_anoy.append((mp[request.person1],mp[request.person2]))
  antirequest_anoy = []
  for request in antirequests:
    antirequest_anoy.append((mp[request.person1],mp[request.person2]))
  return request_anoy, antirequest_anoy, mp
rooms = {}
leftovers = {"Boy": [], "Girl": []} # again, do not talk about this publicly
for sector in sectors:
  reqs, antireqs, mp = anonymize(sector)
  sz = len(students_by_sector[sector])
  inv = {v: k for k, v in mp.items()}
  if not sz:
    rooms[sector] = []
    continue
  res = solve(sz, m, reqs, antireqs)
  print("\n\n\n\n")
  # print(sz)
  lst = [[]] * len(res)
  for a in res:
    if len(res[a]) == m:
      vals = res[a]
      lst[a] = [inv[val] for val in vals]
    else:
      for b in res[a]:
        leftovers[sector[:-1]].append(inv[b])
  if lst[-1] == []:
    lst = lst[:-1]
  rooms[sector] = lst

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
rooms["BoyL"] = list(chunker(leftovers["Boy"], 4))
rooms["GirlL"] = list(chunker(leftovers["Girl"], 4))
print("Saving draft arrangements to draftrooms.csv and draftpeople.csv")
roomcsv = open('draftrooms.csv', mode='w', newline='')
roomdata = []
writer = csv.writer(roomcsv, dialect='excel')
writer.writerow(["Room ID", "Sector", "Ordinal", "Room #", "People"])
curroom = -1
overflowcnt = 0
for s in rooms:
  sector_of_rooms = rooms[s]
  # print(sector_of_rooms)
  cnt = 1
  for room in sector_of_rooms:
    curroom += 1
    try:
      while str(roomnums[curroom]) == '325':
        row = [curroom, 'resv', '', str(roomnums[curroom])]
        writer.writerow(row)
        roomdata.append(row)
        # print(row)
        curroom += 1
    except IndexError:
      pass
    row = []
    try:
      row = [curroom, s, cnt, str(roomnums[curroom])]
    except IndexError:
      overflowcnt += 1
      row = [curroom, s, cnt, f"Overflow{overflowcnt}"]
    # print(room)
    for person in room:
      #print(s)
      row.append(f"{person.firstname} {person.lastname} {person.grade} ({person.id})")
      person.roomID = curroom
    # print(row)
    writer.writerow(row)
    roomdata.append(row)
    cnt += 1
while True:
  try:
    curroom += 1
    writer.writerow([curroom, 'extra', '', str(roomnums[curroom])])
    roomdata.append(row)
  except IndexError:
    break
roomcsv.close()

peoplecsv = open('draftpeople.csv', mode='w', newline='')
writer2 = csv.writer(peoplecsv, dialect='excel')
writer2.writerow(["ID", "Last", "First", "Grade", "Gender", "Room #", "Room ID", "Sector"])
print(students)
for student in students:
  writer2.writerow([student.id, student.lastname, student.firstname, student.grade, student.gender, roomdata[student.roomID][3], student.roomID, roomdata[student.roomID][1]])
peoplecsv.close()

"""Room adjustments"""
print("\n\n\n-----Room Adjustments-----")
while True:
  try:
    option = int(input("""1 to adjust students,
2 to rename room,
3 to view rooms,
4 to exit and download new CSV.
Enter choice: """))
  except:
    print("Invalid Input")
    continue
  if option == 4:
    break
  if option == 1:
    try:
      identi = int(input("Person ID: "))
      toroom = int(input("to Room ID: "))
    except ValueError:
      print("Value error. Discarding operation")
      continue
    confirm = input("CONFIRM: Put n here (no spaces etc) to discard operation, anything else to continue: ")
    if confirm == 'n':
      print("Discarding Operation")
      continue
    person = students[identi]
    person.roomID = toroom
    for room in roomdata:
      try:
        room.remove(f"{person.firstname} {person.lastname} {person.grade} ({person.id})")
      except ValueError:
        pass
    roomdata[toroom].append(f"{person.firstname} {person.lastname} {person.grade} ({person.id})")
    print("Done")
  if option == 2:
    try:
      roomid = int(input("Room ID: "))
      roomsector = (input("Room Sector name to rename to: "))
      roomord = int(input("Room Ordinal to rename to: "))
    except ValueError:
      print("Value error. Discarding operation")
      continue
    confirm = input("CONFIRM: Put n here (no spaces etc) to discard operation, anything else to continue: ")
    if confirm == 'n':
      print("Discarding Operation")
      continue
    roomdata[roomid][1] = roomsector
    roomdata[roomid][2] = roomord
    print("Done")
  if option == 3:
    print("===STUDENTS DATA===\n")
    for student in students:
      print([student.id, student.lastname, student.firstname, student.grade, student.gender, roomdata[student.roomID][3], student.roomID, roomdata[student.roomID][1]])
    print("\n===ROOM DATA===")
    for room in roomdata:
      print(room)

print("Writing final rooms to finalrooms.csv and finalpeople.csv")
finalrooms = open('finalrooms.csv', mode='w', newline='')
writer_finalrooms = csv.writer(finalrooms, dialect='excel')
writer_finalrooms.writerow(["Room ID", "Sector", "Ordinal", "Room #", "People"])
for room in roomdata:
  writer_finalrooms.writerow(room)
finalrooms.close()
#files.download('finalrooms.csv')
finalpeople = open('finalpeople.csv', mode='w', newline='')
writer_finalpeople = csv.writer(finalpeople, dialect='excel')
writer_finalpeople.writerow(["ID", "Last", "First", "Grade", "Gender", "Room #", "Room ID", "Sector"])
for student in students:
  writer_finalpeople.writerow([student.id, student.lastname, student.firstname, student.grade, student.gender, roomdata[student.roomID][3], student.roomID, roomdata[student.roomID][1]])
finalpeople.close()
#files.download('finalpeople.csv')
input("Press RETURN to exit. ")

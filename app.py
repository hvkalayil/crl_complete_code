from flask import Flask, render_template, url_for, request, redirect , session , send_file ,flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView ,expose
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin , LoginManager , current_user , login_user
from base64 import b64encode
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
import urllib.error ,urllib.parse , urllib.request
import json
import scholarly
import os

# APP CONFIG, DB , ADMIN , LOGIN--------------------------------------------

app = Flask(__name__)

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iit.db'
app.config['SECRET_KEY'] = 'crladmin'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

login = LoginManager(app)
@login.user_loader
def load_user(user_id):
    return adminTable.query.get(user_id)
# ----------------------------------------------------------------------------

#IMAGE UPLOADS----------------------------------------------------------------
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin/home_up', methods=['POST'])
def home_upload():
    file = request.files['file']
    if file.filename == '':
        return 'Select a file first.<br><a href=\"/admin/home_upload\">Go Back</a>'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = app.config['UPLOAD_FOLDER'] + '/home'
        file.save(os.path.join(path, filename))
        task = HomePageImage(name=filename)
        try:
            db.session.add(task)
            db.session.commit()
        except:
            return '''Couldnot add filename to database.<br>
            Try again with the same file, if it was uploaded it will be overwritten.<br>
            <a href=\"/admin/home_upload\">Go Back</a>'''

        return '''
        Image Upload Sucessful<br>
        The image will be saved in static/uploads/home
        <a href=/admin/home_upload>Go Back</a>'''

@app.route('/admin/upload', methods=['POST'])
def people_upload():
    file = request.files['file']
    pid = request.form['peopleId']
    if file.filename == '':
        return 'Select a file first.<br><a href=\"/admin/upload\">Go Back</a>'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = app.config['UPLOAD_FOLDER'] + '/people'
        file.save(os.path.join(path, filename))
        task = PeopleImage(people_id=pid,name=filename)
        try:
            db.session.add(task)
            db.session.commit()
        except:
            return '''Couldnot add filename to database.<br>
            Try again with the same file, if it was uploaded it will be overwritten.
            <br><a href=\"/admin/upload\">Go Back</a>'''

        return '''
        Image Upload Sucessful<br>
        The image will be saved in static/uploads/people
        <a href=/admin/upload>Go Back</a>'''

@app.route('/admin/research_up', methods=['POST'])
def research_upload():
    file = request.files['file']
    title = request.form['title']
    if file.filename == '':
        return 'Select a file first.<br><a href=\"/admin/research_upload\">Go Back</a>'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = app.config['UPLOAD_FOLDER'] + '/research'
        file.save(os.path.join(path, filename))
        task = ResearchImage(titles=title,name=filename)
        try:
            db.session.add(task)
            db.session.commit()
        except:
            return '''Couldnot add filename to database.<br>
            Try again with the same file, if it was uploaded it will be overwritten.
            <br><a href=\"/admin/research_upload\">Go Back</a>'''
        return '''
        Image Upload Sucessful<br>
        The image will be saved in static/uploads/research
        <a href=/admin/research_upload>Go Back</a>'''

@app.route('/admin/facility_up', methods=['POST'])
def facility_upload():
    file = request.files['file']
    if file.filename == '':
        return 'Select a file first.<br><a href=\"/admin/facility_upload\">Go Back</a>'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = app.config['UPLOAD_FOLDER'] + '/facility'
        file.save(os.path.join(path, filename))
        task = FacilityImage(name=filename)
        try:
            db.session.add(task)
            db.session.commit()
        except:
            return '''Couldnot add filename to database.<br>
            Try again with the same file, if it was uploaded it will be overwritten.
            <br><a href=\"/admin/facility_upload\">Go Back</a>'''
        return '''
        Image Upload Sucessful<br>
        The image will be saved in static/uploads/facility
        <a href=/admin/facility_upload>Go Back</a>'''

# ----------------------------------------------------------------------------

# DB TABLES---------------------------------------------------------------------

class adminTable(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(10) , default='crladmin')
    pwd = db.Column(db.String(30), default='crl1234')

    def __repr__(self):
        return '<adminTable %r>' % self.id

class HomePage(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    text = db.Column(db.String(500))

class HomePageImage(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(50))

class PeopleImage(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    people_id = db.Column(db.Integer)
    name = db.Column(db.String(50))

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer , primary_key=True)
    people_id = db.Column(db.Integer)
    name = db.Column(db.String(30))
    designation = db.Column(db.String(30))
    details = db.Column(db.String(50))
    address = db.Column(db.String(100))

class Contacts(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer , primary_key=True)
    people_id = db.Column(db.Integer)
    details = db.Column(db.String(30))

class Academics(db.Model):
    __tablename__ = 'academics'
    id = db.Column(db.Integer , primary_key=True)
    people_id = db.Column(db.Integer)
    degree = db.Column(db.String(100))
    year = db.Column(db.Integer)
    university = db.Column(db.String(200))
    remarks = db.Column(db.String(200))

class Research(db.Model):
    __tablename__ = 'research'
    id = db.Column(db.Integer , primary_key=True)
    people_id = db.Column(db.Integer)
    text = db.Column(db.Unicode())

class Positions(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer , primary_key=True)
    people_id = db.Column(db.Integer)
    date = db.Column(db.String(30))
    position = db.Column(db.String(30))
    organization = db.Column(db.String(100))
    link = db.Column(db.String(100))

class Awards(db.Model):
    __tablename__ = 'awards'
    id = db.Column(db.Integer , primary_key=True)
    people_id = db.Column(db.Integer)
    text = db.Column(db.String(200))
    link = db.Column(db.String(200))

class Papers(db.Model):
    __tablename__ = 'papers'
    id = db.Column(db.Integer , primary_key=True)
    people_id = db.Column(db.Integer)
    name = db.Column(db.String(200))
    year = db.Column(db.Integer)
    citations = db.Column(db.Integer)
    journal = db.Column(db.String(100))
    link = db.Column(db.String(100))

class ResearchPage(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    interests = db.Column(db.String(500))

class ResearchImage(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    titles = db.Column(db.String(100))
    name = db.Column(db.String(50))

class ComputationalFacilities(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    facility = db.Column(db.String(500))

class ExperimentalFacilities(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    facility = db.Column(db.String(500))

class FacilityImage(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(30))

class TypesOfLinks(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    type = db.Column(db.String(50))
    type_id = db.Column(db.Integer)

class InterestingLinks(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    type_id = db.Column(db.Integer)
    text = db.Column(db.String(300))
    link = db.Column(db.String(300))

class MTech(db.Model):
    __tablename__ = 'mtech'
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(50))

# --------------------------------------------------------------------------------


# LOGIN LOGOUT UPLOAD ------------------------------------------------------------

@app.route('/login',methods=['POST' , 'GET'])
def login():
    error = False
    if adminTable.query.all() == []:
        firstTime = True
    else:
        firstTime = False
    if request.method == 'POST':
        task = adminTable.query.get(1)
        name = request.form['name']
        formPwd = request.form['formPwd']

        if formPwd == task.pwd and name == task.name:
            login_user(task)
            return redirect('admin')
        else:
            error = True
            return render_template('login.html',state=error,time=firstTime)
    return render_template('login.html',state=error,time=firstTime)

@app.route('/logout')
def logout():
    db.session.commit()
    session.clear()
    return redirect('/login')   

@app.route('/updateCheck/<int:pid>',methods=['POST'])
def updateCheck(pid):
    peopleName = People.query.filter_by(people_id=pid).first().name
    queryName = peopleName + ', IIT Bombay'
    try:
        search_query = scholarly.search_author(queryName)
    except:
        return 'It looks like we are not getting data for ' + queryName + '. Maybe there is some network issue'

    author = next(search_query).fill()
    total = len([pub.bib['title'] for pub in author.publications])
    count = Papers.query.filter_by(people_id=pid).count()
    if total-count == 0:
        short = 'Papers are up to date'
    else:
        short = str(total-count) + ' papers can be updated from Google Scholar'
    
    return render_template('admin/updatePapers.html',msg=short,old=count,pid=pid,total=total)

@app.route('/updatePapers/<int:pid>',methods=['POST'])
def updatePapers(pid):
    peopleName = People.query.filter_by(people_id=pid).first().name
    queryName = peopleName + ', IIT Bombay'
    try:
        search_query = scholarly.search_author(queryName)
    except:
        return 'It looks like we are not getting data for ' + queryName + '. Maybe there is some network issue'

    author = next(search_query).fill()
    lowerLimit = int(request.form['lb'])
    upperLimit = int(request.form['ub'])
    updatedRecords = 0
    newRecords = 0

    for i in range(lowerLimit,upperLimit):
        title = author.publications[i].bib['title']
        tableTitle = Papers.query.filter_by(people_id=pid,name=title).all()
        try:
            data = author.publications[i].fill()
        except:
            if tableTitle == []:
                task = Papers(people_id=pid,name=title)
                try:
                    db.session.add(task)
                    db.session.commit()
                    newRecords = newRecords + 1
                except:
                    return 'ERROR when adding new Record.'
        
        try:
            journ = data.bib['journal']
        except:
            journ = 'None'
        try:
            url = data.bib['url']
        except:
            url = 'None'
        try:
            yr = data.bib['year']
        except:
            yr = 'None'
        try:
            citedby = data.citedby
        except:
            citedby = 'None'

        if tableTitle == []:
            task = Papers(people_id=pid,name=title,year=yr,citations=citedby,journal=journ,link=url)
            try:
                db.session.add(task)
                db.session.commit()
                newRecords = newRecords + 1
            except:
                return 'ERROR when adding new Record.'
        else:
            new = Papers.query.filter_by(people_id=pid,name=title).first()
            if new.year == yr and new.citations == citedby and new.journal == journ and new.link == url:
                continue
            new.year = yr
            new.citations = citedby
            new.journal = journ
            new.link = url
            try:
                db.session.commit()
                updatedRecords = updatedRecords + 1
            except:
                return 'ERROR when updating existing Record.'

    short = str(newRecords) + ' papers were added.<br>' + str(updatedRecords) + ' papers were updated'
    return short + '<a href=\"/admin/papers\">View here</a><br><a href=\"/admin/update\">Add Another</a>'
# --------------------------------------------------------------------------------


# ADMIN VIEWS---------------------------------------------------------------------
class RestrictModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class UploadPicture(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

    @expose('/')
    def index(self):
        tasks = People.query.all()
        images = PeopleImage.query.all()
        pics = []
        for task in tasks:
            for img in images:
                if img.people_id == task.people_id:
                    pics.append(img.name)
                    break
        return self.render('admin/upload.html',tasks=tasks,path=pics)

class UploadResearchPicture(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

    @expose('/')
    def index(self):
        images = ResearchImage.query.all()
        globalArray = []
        subArray = ''
        imgsubArray = []
        finalArray = []
        finalimgArray = []
        for img in images:
            if img.titles in globalArray:
                continue
            else:
                globalArray.append(img.titles)
                for i in images:
                    if img.titles == i.titles:
                        subArray = i.titles
                        imgsubArray.append(i)
                finalArray.append(subArray)
                finalimgArray.append(imgsubArray)
                subArray = []
                imgsubArray = []

        return self.render('admin/research_upload.html',
        finalArray=finalArray,finalimgArray=finalimgArray)

class UploadHomepagePicture(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

    @expose('/')
    def index(self):
        table = HomePageImage.query.all()
        return self.render('admin/home_upload.html',table=table)

class UploadFacilityPicture(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

    @expose('/')
    def index(self):
        table = FacilityImage.query.all()
        return self.render('admin/facility_upload.html',table=table)

class UpdatePapers(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

    @expose('/')
    def index(self):
        peopleTable = People.query.all()
        designationList = ['Professor','Research Associate','Ph.D']
        finalPeople = []
        finalCount = []
        for item in peopleTable:
            if item.designation in designationList:
                count = Papers.query.filter_by(people_id=item.people_id).count()
                finalPeople.append(item)
                finalCount.append(count)
        return self.render('admin/update.html',finalPeople=finalPeople,finalCount=finalCount)

class ImageModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    column_list = ['name']

class ResearchImageModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    column_list = ['titles']
    
admin = Admin(app)
admin.add_link(MenuLink(name='LogOut',category='', url="/logout"))
admin.add_views(
    RestrictModelView(adminTable,db.session),
    
    RestrictModelView(HomePage,db.session , category='Home Page'),
    UploadHomepagePicture(name='Upload HomePage Images' , endpoint='home_upload' , category='Home Page'),
    ImageModelView(HomePageImage,db.session , category='Home Page'),

    RestrictModelView(People,db.session,category='People Page'),
    UploadPicture(name='Upload Image' , endpoint='upload' , category='People Page'),
    ImageModelView(PeopleImage,db.session,category='People Page'),
    RestrictModelView(Contacts,db.session,category='People Page'),
    RestrictModelView(Academics,db.session,category='People Page'),
    RestrictModelView(Research,db.session,category='People Page'),
    RestrictModelView(Awards,db.session,category='People Page'),
    RestrictModelView(Positions,db.session,category='People Page'),
    RestrictModelView(Papers,db.session,category='People Page'),
    UpdatePapers(name='Update Papers' , endpoint='update' , category='People Page'),
    RestrictModelView(MTech,db.session,category='People Page'),

    RestrictModelView(ResearchPage,db.session,category='Research Page'),
    UploadResearchPicture(name='Upload Research Image' , endpoint='research_upload' , category='Research Page'),
    ResearchImageModelView(ResearchImage,db.session,category='Research Page'),

    RestrictModelView(ComputationalFacilities,db.session,category='Facilities Page'),
    RestrictModelView(ExperimentalFacilities,db.session,category='Facilities Page'),
    UploadFacilityPicture(name='Upload Facility Image' , endpoint='facility_upload' , category='Facilities Page'),
    ImageModelView(FacilityImage,db.session , category='Facilities Page'),

    RestrictModelView(TypesOfLinks,db.session,category='Interesting Links Page'),
    RestrictModelView(InterestingLinks,db.session,category='Interesting Links Page'),

    )

# ----------------------------------------------------------------------------------


# ROUTES----------------------------------------------------------------------------
@app.route('/default',methods=['POST'])
def default():
    defaultAdmin = adminTable(name='admin',pwd='crl1234')
    db.session.add(defaultAdmin)    
    db.session.commit()

    login_user(defaultAdmin)
    return redirect('admin')

@app.route('/')
def index():
    tasks = HomePage.query.get(1)
    table = HomePageImage.query.all()
    return render_template('index.html',tasks=tasks,images=table)

@app.route('/people')
def people():

    mtech = MTech.query.all()

    tasks = People.query.all()
    
    globalList = ['Professor','Postdoctoral Researcher',
    'Research Associate','Ph.D','Research Staff','M.Tech','Alumni']
    subArray = []
    subimgArray = []
    finalArray = []
    images = []
    for item in globalList:
        for man in tasks:
            if item == man.designation:
                pic = PeopleImage.query.filter_by(people_id=man.people_id).first()
                subArray.append(man)
                if pic is None:
                    subimgArray.append('#')
                else:
                    subimgArray.append(pic)
                
        finalArray.append(subArray)
        images.append(subimgArray)
        subArray = []
        subimgArray = []
    return render_template('people.html',images = images,
    finalArray=finalArray,globalList=globalList,mtech=mtech)

@app.route('/individual/<int:pid>',methods=['GET'])
def individual(pid):

    table = PeopleImage.query.filter_by(people_id=pid).first()
    ctitle = []
    clink = []
    pubs = []
    people = People.query.filter_by(people_id=pid).all()
    contacts = Contacts.query.filter_by(people_id=pid).all()
    academics = Academics.query.filter_by(people_id=pid).all()
    research = Research.query.filter_by(people_id=pid).all()
    positions = Positions.query.filter_by(people_id=pid).all()
    awards = Awards.query.filter_by(people_id=pid).all()
    papers = Papers.query.filter_by(people_id=pid).order_by(Papers.year.desc()).all()
    for item in papers:
        if item.year == 'None' or item.journal == 'None' or item.year == None or item.journal == None:
            ctitle.append(item.name)
            try:
                clink.append(item.link)
            except:
                clink.append('#')
        else:
            pubs.append(item)

    return render_template('individual.html',
    people=people,image=table,
    contacts=contacts,
    academics=academics,research=research,awards=awards,positions=positions,
    pubs=pubs,ctitle=ctitle,clink=clink)
    
@app.route('/research')
def research():
    tasks = ResearchPage.query.all()
    images = ResearchImage.query.all()
    globalArray = []
    imgsubArray = []
    finalimgArray = []
    for img in images:
        if img.titles in globalArray:
            continue
        else:
            globalArray.append(img.titles)
            for i in images:
                if img.titles == i.titles:
                    imgsubArray.append(i)
            finalimgArray.append(imgsubArray)
            imgsubArray = []

    return render_template('research.html',tasks=tasks,
    finalArray=globalArray,finalimgArray=finalimgArray)

@app.route('/publications')
def publications():
    tasks = Papers.query.order_by(Papers.year.desc()).all()
    finalArray = []
    for item in tasks:
        if item.year == 'None' or item.journal == 'None' or item.year == None or item.journal == None:
            continue
        else:
            finalArray.append(item)
    
    globalList = []
    subArray = []
    fArray = []
    for item in finalArray:
        if item.year in globalList:
            continue
        else:
            globalList.append(item.year)
            for nxt in finalArray:
                if item.year == nxt.year:
                    subArray.append(nxt)
            fArray.append(subArray)
            subArray = []
    return render_template('publications.html',tasks=fArray,globalList=globalList)
    
@app.route('/facilities')
def facilities():
    comp = ComputationalFacilities.query.all()
    exp = ExperimentalFacilities.query.all()
    images = FacilityImage.query.all()
    return render_template('facilities.html',comp=comp,exp=exp,images=images)
    
@app.route('/interestingLinks')
def interestingLinks():
    typeOfLinks = TypesOfLinks.query.all()
    iLinks = InterestingLinks.query.all()
    subArray = []
    finalArray = []
    types = []
    for item in typeOfLinks:
        for part in iLinks:
            if item.type_id == part.type_id:
                subArray.append(part)
        finalArray.append(subArray)
        types.append(item.type)
        subArray = []
    return render_template('interestingLinks.html',finalArray=finalArray,types=types)
if __name__ == '__main__':
    app.run(debug=True)
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, jsonify, send_from_directory
from flask.ext.login import login_required, current_user
from . import demography
from .forms import PageForm
from .. import db
from ..spandex.models import Permission, Role, User, Project, Publication
from ..models import Plant, Page, Upload, OldSpecies, OldPlant
from ..models import Species as Sp
from ..decorators import admin_required
import re, sys, os
from jinja2 import evalcontextfilter, Markup, escape
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from werkzeug import secure_filename
import pydot
import itertools
from itertools import islice


sys.path.append('/Users/francesca/sites/env/life-cycle')

@demography.route('/')
def map():

	species = OldSpecies.query.all()
	plants = OldPlant.query.all()

	return render_template('map.html', plants=plants, species=species)


@demography.route('/geojson/all')
def geojson():

	geojson = {
	'type' : 'FeatureCollection',
	'features' : []
	}

	plants = OldPlant.query.all()

	for plant in plants:
		longi = plant.longitudedec
		lati = plant.latitudedec

		if longi == 'NA':
			pass

		elif lati == 'NA':
			pass

		else:

			fe = {
					'type' : 'Feature',
					'geometry' : {
						'type' : 'Point',
						'coordinates' : [plant.longitudedec, plant.latitudedec]
					},
					'properties' : {
						'title' : '<em>'+plant.name+'</em>',
						'name' : plant.name,
						'matrixnumber' : plant.matrixnumber,
						'matrix' : plant.matrix,
						'dimension' : plant.dimension,
						'matrixclassnumber' : plant.matrixclassnumber,
						'matrixclassorganised' : plant.matrixclassorganised,
						'matrixsplit' : plant.matrixsplit,
						'classnames' : plant.classnames,
						'observation' : plant.observation,
						'matrixcomposite' : plant.matrixcomposite,
						'matrixtreatment' : plant.matrixtreatment,
						'matrixcaptivity' : plant.matrixcaptivity,
						'matrixstartyear' : plant.matrixstartyear,
						'matrixstartseason' : plant.matrixstartseason,
						'matrixstartmonth' : plant.matrixstartmonth,
						'matrixendyear' : plant.matrixendyear,
						'matrixendseason' : plant.matrixendseason,
						'matrixendmonth' : plant.matrixendmonth,
						'studiedsex' : plant.studiedsex,
						'population' : plant.population,
						'latdeg' : plant.latdeg,
						'latmin' : plant.latmin,
						'latsec' : plant.latsec,
						'londeg' : plant.londeg,
						'lonmin' : plant.lonmin,
						'lonsec' : plant.lonsec,
						'altitude' : plant.altitude,
						'country' : plant.country,
						'continent' : plant.continent,
						'criteriasize' : plant.criteriasize,
						'criteriaontogeny' : plant.criteriaontogeny,
						'authors' : plant.authors,
						'journal': plant.journal,
						'yearpublication' : plant.yearpublication,
						'doiisbn' : plant.doiisbn,
						'enteredby' : plant.enteredby,
						'entereddate' : plant.entereddate,
						'source' : plant.source,
						'statusstudy' : plant.statusstudy,
						'statusstudyref' : plant.statusstudyref,
						'statuselsewhere' : plant.statuselsewhere,
						'statuselsewhereref' : plant.statuselsewhereref,
						'marker-color' : '#e74c3c',
						'marker-size' : 'small',
						'species' : {
							'name' : plant.species.name,
							'speciesauthor' : plant.species.speciesauthor,
							'kingdom' : plant.species.kingdom,
							'phylum' : plant.species.phylum,
							'angiogymno' : plant.species.angiogymno,
							'dicotmonoc' : plant.species.dicotmonoc,
							'class' : plant.species._class,
							'order' : plant.species._order,
							'family': plant.species.family,
							'genus' : plant.species.genus,
							'ecoregion' : plant.species.ecoregion,
							'growthtype' : plant.species.growthtype,
							'growthformraunkiaer' : plant.species.growthformraunkiaer,
							'annualperiodicity' : plant.species.annualperiodicity,
							'planttype' : plant.species.planttype,
							'commonname' : plant.species.commonname,
							'originalimageurl' : plant.species.originalimageurl,
							'localimageurl' : plant.species.localimageurl,
							'originalpageurl' : plant.species.originalpageurl
							}
						}
					
				}


			geojson["features"].append(fe)


	return jsonify(geojson)

@demography.route('/ecoregion')
def ecoregion():

	ecoregion = {
	'TMB' : ['Terrestrial', str('Tropical and subtropical moist broadleaf forests.')],
	'TDB' : ['Terrestrial', str('Tropical and subtropical dry broadleaf forests.')],
	'TSC' : ['Terrestrial', str('Tropical and subtropical coniferous forests.')], 
	'TBM' : ['Terrestrial', str('Temperate broadleaf and mixed forests.')],
	'TCF' : ['Terrestrial', str('Temperate coniferous forests.')],
	'BOR' : ['Terrestrial', str('Boreal forests/taiga.')],
	'TGV' : ['Terrestrial', str('Tropical and subtropical grasslands, savannas and shrublands.')],
	'TGS' : ['Terrestrial', str('Temperate grasslands, savannas, and shrublands.')],
	'FGS' : ['Terrestrial', str('Flooded grasslands, savannas, and shrublands.')],
	'MON' : ['Terrestrial', str('Montane grasslands and shrublands.')],
	'TUN' : ['Terrestrial', str('Tundra.')],
	'MED' : ['Terrestrial', str('Mediterranean forests, woodlands and scrubs.')],
	'DES' : ['Terrestrial', str('Deserts and xeric shrublands.')],
	'MAN' : ['Terrestrial', str('Mangroves.')],
	'LRE' : ['Freshwater', str('Large river ecosystems.')],
	'LRH' : ['Freshwater', str('Large river headwater ecosystems.')],
	'LRD' : ['Freshwater', str('Large river delta ecosystems.')],
	'SRD' : ['Freshwater', str('Small river delta ecosystems.')],
	'SLE' : ['Freshwater', str('Small lake ecosystems.')],
	'LLE' : ['Freshwater', str('Large lake ecosystems')],
	'XBE' : ['Freshwater', str('Xeric basin ecosystems.')],
	'POE' : ['Marine', str('Polar ecosystems.')],
	'TSS' : ['Marine', str('Temperate shelf and seas ecosystems.')],
	'TEU' : ['Marine', str('Temperate upwellings.')],
	'TRU' : ['Marine', str('Tropical upwellings.')],
	'TRC' : ['Marine', str('Tropical coral.')],
	'LAB' : ['Laboratory or greenhouse conditions controlled, usually indoor, conditions that mean the study species is not affected by the environment conditions typical of the actual geographic location of the study.']
	}

	return jsonify(ecoregion)

@demography.route('/geojson/<param>/<filters>')
def geojsonfilter(param, filters):

	kwargs = {
		param : filters
	}

	geojson = {
	'type' : 'FeatureCollection',
	'features' : []
	}


	plants = OldPlant.query.filter_by(**kwargs)

	for plant in plants:
		longi = plant.longitudedec
		lati = plant.latitudedec

		if longi == 'NA':
			pass

		elif lati == 'NA':
			pass

		else:
			fe = {
					'type' : 'Feature',
					'geometry' : {
						'type' : 'Point',
						'coordinates' : [plant.longitudedec, plant.latitudedec]
					},
					'properties' : {
						'title' : '<em>'+plant.name+'</em>',
						'name' : plant.name,
						'matrixnumber' : plant.matrixnumber,
						'matrix' : plant.matrix,
						'dimension' : plant.dimension,
						'matrixclassnumber' : plant.matrixclassnumber,
						'matrixclassorganised' : plant.matrixclassorganised,
						'matrixsplit' : plant.matrixsplit,
						'classnames' : plant.classnames,
						'observation' : plant.observation,
						'matrixcomposite' : plant.matrixcomposite,
						'matrixtreatment' : plant.matrixtreatment,
						'matrixcaptivity' : plant.matrixcaptivity,
						'matrixstartyear' : plant.matrixstartyear,
						'matrixstartseason' : plant.matrixstartseason,
						'matrixstartmonth' : plant.matrixstartmonth,
						'matrixendyear' : plant.matrixendyear,
						'matrixendseason' : plant.matrixendseason,
						'matrixendmonth' : plant.matrixendmonth,
						'studiedsex' : plant.studiedsex,
						'population' : plant.population,
						'latdeg' : plant.latdeg,
						'latmin' : plant.latmin,
						'latsec' : plant.latsec,
						'londeg' : plant.londeg,
						'lonmin' : plant.lonmin,
						'lonsec' : plant.lonsec,
						'altitude' : plant.altitude,
						'country' : plant.country,
						'continent' : plant.continent,
						'criteriasize' : plant.criteriasize,
						'criteriaontogeny' : plant.criteriaontogeny,
						'authors' : plant.authors,
						'journal': plant.journal,
						'yearpublication' : plant.yearpublication,
						'doiisbn' : plant.doiisbn,
						'enteredby' : plant.enteredby,
						'entereddate' : plant.entereddate,
						'source' : plant.source,
						'statusstudy' : plant.statusstudy,
						'statusstudyref' : plant.statusstudyref,
						'statuselsewhere' : plant.statuselsewhere,
						'statuselsewhereref' : plant.statuselsewhereref,
						'marker-color' : '#e74c3c',
						'marker-size' : 'small',
						'species' : {
							'name' : plant.species.name,
							'speciesauthor' : plant.species.speciesauthor,
							'kingdom' : plant.species.kingdom,
							'phylum' : plant.species.phylum,
							'angiogymno' : plant.species.angiogymno,
							'dicotmonoc' : plant.species.dicotmonoc,
							'class' : plant.species._class,
							'order' : plant.species._order,
							'family': plant.species.family,
							'genus' : plant.species.genus,
							'ecoregion' : plant.species.ecoregion,
							'growthtype' : plant.species.growthtype,
							'growthformraunkiaer' : plant.species.growthformraunkiaer,
							'annualperiodicity' : plant.species.annualperiodicity,
							'planttype' : plant.species.planttype,
							'commonname' : plant.species.commonname,
							'originalimageurl' : plant.species.originalimageurl
							}
						}
					
				}


			geojson["features"].append(fe)

	return jsonify(geojson)

@demography.route('/speciesjson/<name>')
def speciesjson(name):


	geojson = {
	'type' : 'FeatureCollection',
	'features' : []
	}

	kwargs = {
	'name' : name
	}

	species = OldSpecies.query.filter_by(**kwargs)

	for sp in species:

		if sp.name == 'NA':
			fe = {
			'name' : 'Not Enough Data'
			}
			

		else:
			fe = {
					'name' : sp.name,
					'speciesauthor' : sp.speciesauthor,
					'kingdom' : sp.kingdom,
					'phylum' : sp.phylum,
					'angiogymno' : sp.angiogymno,
					'dicotmonoc' : sp.dicotmonoc,
					'class' : sp._class,
					'order' : sp._order,
					'family': sp.family,
					'genus' : sp.genus,
					'ecoregion' : sp.ecoregion,
					'growthtype' : sp.growthtype,
					'growthformraunkiaer' : sp.growthformraunkiaer,
					'annualperiodicity' : sp.annualperiodicity,
					'planttype' : sp.planttype,
					'commonname' : sp.commonname,
					'originalimageurl' : sp.originalimageurl,
					'localimageurl' : sp.localimageurl,
					'originalpageurl' : sp.originalpageurl
						}
					
				


			geojson['features'].append(fe)

	return jsonify(geojson)

@demography.route('/json/image/<name>')
def jsonimage(name):

	kwargs = {
		'name' : name
	}

	species = OldSpecies.query.filter_by(**kwargs).first()

	json = {
		'url' : species.localimageurl
	}

	return jsonify(json)

@demography.route('/pages/')
@login_required 
def pages():

    pages = Page.query.all()

    return render_template('pages.html', pages=pages)

@demography.route('/pages/<int:id>')
@login_required 
def page(id):
    kwargs = {
    'id' : id
    }

    page = Page.query.filter_by(**kwargs).first_or_404()

    return render_template('page.html', page=page)

@demography.route('/pages/edit/<int:id>', methods=['GET', 'POST'])
@login_required 
def pageedit(id):
	kwargs = {
	'id' : id
	}

	page = Page.query.filter_by(**kwargs).first_or_404()

	if current_user != page.researcher and \
		not current_user.can(Permission.WRITE_ARTICLES): abort(403)
	form = PageForm()
	if form.validate_on_submit():
		page.title = form.title.data
		page.content = form.content.data
		page.project_name = 'demography'
		page.publish = form.publish.data
		page.researcher = current_user._get_current_object()

		db.session.add(page)
		flash('The page has been updated.')
		return redirect(url_for('.page', id=page.id))

	form.title.data = page.title
	form.content.data = page.title
	form.publish.data = page.publish
	return render_template('edit_page.html', page=page, form=form)

@demography.route('/pages/add', methods=['GET', 'POST'])
@login_required 
def pageadd():
	page = Page()

	if current_user != page.researcher and \
		not current_user.can(Permission.WRITE_ARTICLES): abort(403)
	
	form = PageForm()
	
	if form.validate_on_submit():
		page.title = form.title.data
		page.content = form.content.data
		page.project_name = 'demography'
		page.publish = form.publish.data
		page.researcher = current_user._get_current_object()

		db.session.add(page)
		flash('The page has been updated.')
		return redirect(url_for('.map'))
	return render_template('post_page.html', page=page, form=form)

@demography.route('/add/')
@login_required
def add():
	return render_template('upload.html')

@demography.route('/doi/')
@login_required
def doi():
	m = OldPlant.query.order_by(Plant.id.desc()).first()

	return render_template('doi.html', m=m)


import app
def stringFromText(string):
	#Formatting string and separating for use as a list
	#string usually contained within [], remove these
	if string.startswith('[') and string.endswith(']'):
	    string = string[1:-1]

	 
	#substitute non-alphanumeric with a space
	#string = re.sub('[^\w.\s-+]+', ' ', string)

	# string = string.replace(';', ' ')

	#split into list by whitespace

	#string = [float(x.strip()) for x in string.split(' ')]
	matrix = []
	xl = string.split(' ')
	for x in xl:
		# print x
		if x != '':
			if x == 'NA':
				matrix.append(0)
			else:
				if x == 'NDY':
					matrix.append(0)
				else:
					matrix.append(float(x.strip()))

	return matrix


def classNamesFromText(string):
	classNames = string.split('|')
	# string = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', string)


	# for className in string:
	# 	if className.startswith('"') and className.endswith('"'):
	#    		className = className[1:-1]
	#    		className = className.replace(':', ';')
	#    		classNames.append(className)

	return classNames

def dimensionSquared(classnames, matrix):
	m = len(matrix)
	c = len(classnames)
	s = len(classnames)*len(classnames)

	if s == m:
		return True
	else:
		return False

def dimensionSize(classnames):
	return len(classnames)

def dotGraph(classnames, matrix, matrixnumber, dimension, species):
	graph = pydot.Dot(graph_type='digraph', rankdir="LR")
	#Organise into stages
	classIndices = {}

	#Add classNames to graph as nodes 
	for (i, className) in enumerate(classnames):
		#print className	
		classIndices[className] = i
		graph.add_node(pydot.Node(className, shape="circle"))

	print classIndices

	for rowClassName in classnames:
		row = classIndices[rowClassName]
		for colClassName in classnames:
			col = classIndices[colClassName]
			v = matrix[(row*dimension) + col]
			if v > 0:
				graph.add_edge(pydot.Edge(colClassName, rowClassName, label=str(v)))

	graph.write_svg('static/images/dot/'+str(species)+'_dot.svg', prog='dot')
	return graph

def Species(string):
	species_lower = string.lower()
	species = species_lower.replace(' ', '_')

	return species

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@demography.route('/matrix/', methods=['GET', 'POST'])
@login_required
def matrix():
	return render_template('matrix.html')

@demography.route('/matrixresult/', methods=['GET', 'POST'])
@login_required
def matrixresult():
	classnames = classNamesFromText(request.form['classnames'])
	species = OldSpecies(request.form['species'])
	matrix = stringFromText(request.form['matrix'])
	m = OldPlant.query.order_by(Plant.id.desc()).first()
	matrixnumber = int(m.matrixnumber) + 1
	squared = dimensionSquared(classnames, matrix)
	dimension = dimensionSize(classnames)

	graph = dotGraph(classnames, matrix, matrixnumber, dimension, species)


	return jsonify(classnames=classnames, matrix=matrix, matrixnumber=matrixnumber, squared=squared, dimension=dimension, species=species)

def colour(matrix, fill):
	if matrix != 0.0:
		fill_col = fill
	else:
		fill_col = '#ffffff'
	return fill_col

def matrix_chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def _itersplit(l, splitters):
    current = []
    for item in l:
        if item in splitters:
            yield current
            current = []
        else:
            current.append(item)
    yield current

def magicsplit(l, *splitters):
    return [subl for subl in _itersplit(l, splitters) if subl]

@demography.route('/matrixtable/<int:id>/<which>')
def matrix_table(id, which):
	plant = Plant.query.filter_by(id=id).first()
	
	if which == 'a':
		matrix_str = plant.matrix_a
	if which == 'u':
		matrix_str = plant.matrix_u
	if which == 'f':
		matrix_str = plant.matrix_f
	if which == 'c':
		matrix_str = plant.matrix_c


	dimension = plant.dimension
	classnames_str = plant.classnames
	classnames = classNamesFromText(classnames_str)
	matrix = stringFromText(matrix_str)

	total_values = dimension * dimension

	diag_chunks = list(matrix_chunks(matrix, dimension))
	diag = [ diag_chunks[i][i] for i in range(len(diag_chunks)) ]

	to_colour_prog = []
	to_colour_retro = []	
	
	seps = []
	for n, c in enumerate(diag_chunks):
		if n > 0:
			splitter = c[n]
			seps.append(splitter)
			prog = c[:n]
			retro = c[n+1:]
			to_colour_prog += prog
			to_colour_retro += retro

	progression_growth = to_colour_prog
	retrogression = to_colour_retro


	cells = ""
	
	for i, value in enumerate(matrix):
		value = matrix[i]
		if i <= dimension-1 and i > 0:
			fill_col = '#FF99CB'
		elif value in diag:
			fill_col = '#C0C0C0'
		elif value in progression_growth:
			fill_col = '#CCFFCC'
		elif value in retrogression:
			fill_col = '#FFCC99'
		else: 
			fill_col = '#FFFFFF'

		if i % dimension == 0 and i == 0:
			cells += "<TR><TD border='1' height='30' bgcolor='"+colour(value, fill_col)+"'>" + str(value) + "</TD>"
		elif i % dimension == 0 and i > 0:	
			cells += "</TR><TR><TD border='1' height='30' bgcolor='"+colour(value, fill_col)+"'>" + str(value) + "</TD>"
		else:
			cells += "<TD border='1' height='30' bgcolor='"+colour(value, fill_col)+"'>" + str(value) + "</TD>"

	cells += "</TR>"

	graph = pydot.Dot(graph_type='digraph', rankdir="LR")
	n = pydot.Node('"nodey"', label="<<TABLE border='1' cellspacing='0' cellpadding='2'>"+ cells +"</TABLE>>", shape="none")
	graph.add_node(n)

	filename = "app/static/images/dot/matrix"+ str(plant.id) +"_dot.svg"
	dir = os.path.dirname(filename)
	if not os.path.exists(dir):
		os.makedirs(dir)
	svg = graph.write_svg(filename, prog='dot')	


	return render_template('matrix_svg.html', plant=plant)

@demography.route('/add/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory('/Users/francesca/sites/env/life-cycle/app/uploads', filename)

@demography.route('/add/upload', methods=['POST'])
@login_required
def upload():
	file = request.files['file']
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		upload = Upload()
		upload.filename = filename
		upload.researcher = current_user._get_current_object()
		db.session.add(upload)
		return jsonify(img = filename)

@demography.route('/removecolon/')
def remove_col():
	plants = Plant.query.all()

	for p in plants:
		mat = p.matrix
		p.matrix = mat.replace(';', ' ')

		db.session.add(p)
		db.session.commit()



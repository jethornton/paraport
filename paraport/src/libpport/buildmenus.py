from PyQt5.QtWidgets import (QMenu, QAction, QGridLayout, QLabel,
	QPushButton, QSpacerItem, QSizePolicy)

from libpport import utilities

inputs = [{'Not Used':'Select'},
	{'Homing':['Joint 0 Home', 'Joint 1 Home', 'Joint 2 Home',
		'Joint 3 Home', 'Joint 4 Home', 'Joint 5 Home',
		'Joint 6 Home', 'Joint 7 Home', 'Joint 8 Home', 'Home All']},
	{'Limits':[
		{'Joint 0':['Joint 0 Plus', 'Joint 0 Minus', 'Joint 0 Both']},
		{'Joint 1':['Joint 1 Plus', 'Joint 1 Minus', 'Joint 1 Both']},
		{'Joint 2':['Joint 2 Plus', 'Joint 2 Minus', 'Joint 2 Both']},
		{'Joint 3':['Joint 3 Plus', 'Joint 3 Minus', 'Joint 3 Both']},
		{'Joint 4':['Joint 4 Plus', 'Joint 4 Minus', 'Joint 4 Both']},
		{'Joint 5':['Joint 5 Plus', 'Joint 5 Minus', 'Joint 5 Both']},
		{'Joint 6':['Joint 6 Plus', 'Joint 6 Minus', 'Joint 6 Both']},
		{'Joint 7':['Joint 7 Plus', 'Joint 7 Minus', 'Joint 7 Both']},
		{'Joint 8':['Joint 8 Plus', 'Joint 8 Minus', 'Joint 8 Both']}]},
	{'Jog':[{'X Axis':['Jog X Plus', 'Jog X Minus']},
		{'Y Axis':['Jog Y Plus', 'Jog Y Minus']},
		{'Z Axis':['Jog Z Plus', 'Jog Z Minus']},
		{'A Axis':['Jog A Plus', 'Jog A Minus']},
		{'B Axis':['Jog B Plus', 'Jog B Minus']},
		{'C Axis':['Jog C Plus', 'Jog C Minus']},
		{'U Axis':['Jog U Plus', 'Jog U Minus']},
		{'V Axis':['Jog V Plus', 'Jog V Minus']},
		{'W Axis':['Jog W Plus', 'Jog W Minus']}
	]},
	{'I/O Control':['Flood', 'Mist', 'Lube Level', 'Tool Changed',
		'Tool Prepared', 'External E Stop']},
	{'Motion':['Probe Input', 'Digital 0', 'Digital 1', 'Digital 2', 'Digital 3']}
]

# {'':['', ]},
# '', 
outputs = [{'Not Used':'Select'},
	{'Axes':[
		{'X':['X Step', 'X Direction']},
		{'Y':['Y Step', 'Y Direction']},
		{'Z':['Z Step', 'Z Direction']},
		{'A':['A Step', 'A Direction']},
		{'B':['B Step', 'B Direction']},
		{'C':['C Step', 'C Direction']},
		{'U':['U Step', 'U Direction']},
		{'V':['V Step', 'V Direction']},
		{'W':['W Step', 'W Direction']},
	]},
	{'Spindle':['Spindle On', 'Spindle CW', 'Spindle CCW', 'Spindle Brake']},
	{'I/O Control':['Coolant Flood', 'Coolant Mist', 'Lube Pump',
		'Tool Change', 'Tool Prepare', 'E Stop Out']},
	{'Digital Out':['Digital Out 0', 'Digital Out 1', 'Digital Out 2', 'Digital Out 3', ]}
]

def clearLayout(layout):
	for i in reversed(range(layout.count())):
		layoutItem = layout.itemAt(i)
		if layoutItem.widget() is not None:
			widgetToRemove = layoutItem.widget()
			widgetToRemove.setParent(None)
			layout.removeWidget(widgetToRemove)
		elif layoutItem.spacerItem() is not None:
			pass
		else:
			layoutToRemove = layout.itemAt(i)
			clearLayout(layoutToRemove)

def buildPort1(parent):
	outGrid = parent.pp1outGB.findChild(QGridLayout)
	inGrid = parent.pp1inGB.findChild(QGridLayout)
	verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding) 
	clearLayout(outGrid)
	clearLayout(inGrid)
	parent.p1inBtns = {}
	parent.p1outBtns = {}
	if parent.pp1typeCB.currentData() == 'in':
		outPins = ['1', '14', '16', '17']
		for i in range(len(outPins)):
			outGrid.addWidget(QLabel(f'Pin {outPins[i]}'), i, 0)
			parent.p1outBtns[f'p1OutPB_{i}'] = QPushButton('Select')
			outGrid.addWidget(parent.p1outBtns[f'p1OutPB_{i}'],i , 1)
		outGrid.addItem(verticalSpacer)

		inPins = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '15']
		for i in range(len(inPins)):
			inGrid.addWidget(QLabel(f'Pin {inPins[i]}'), i, 0)
			parent.p1inBtns[f'p1InPB_{i}'] = QPushButton('Select')
			inGrid.addWidget(parent.p1inBtns[f'p1InPB_{i}'],i , 1)
		inGrid.addItem(verticalSpacer)

	elif parent.pp1typeCB.currentData() == 'out':
		outPins = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '14', '16', '17']
		for i in range(len(outPins)):
			outGrid.addWidget(QLabel(f'Pin {outPins[i]}'), i, 0)
			parent.p1outBtns[f'p1OutPB_{i}'] = QPushButton('Select')
			outGrid.addWidget(parent.p1outBtns[f'p1OutPB_{i}'],i , 1)
		outGrid.addItem(verticalSpacer)

		inPins = ['10', '11', '12', '13', '15']
		for i in range(len(inPins)):
			inGrid.addWidget(QLabel(f'Pin {inPins[i]}'), i, 0)
			parent.p1inBtns[f'p1InPB_{i}'] = QPushButton('Select')
			inGrid.addWidget(parent.p1inBtns[f'p1InPB_{i}'],i , 1)
		inGrid.addItem(verticalSpacer)

	if parent.pp1typeCB.currentData():
		for i in range(len(outPins)):
			button = parent.p1outBtns.get(f'p1OutPB_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			menu.triggered.connect(lambda: utilities.setAxisTabs(parent))
			add_menu(outputs, menu)
			button.setMenu(menu)

		for i in range(len(inPins)):
			button = parent.p1inBtns.get(f'p1InPB_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(inputs, menu)
			button.setMenu(menu)


def buildPort2(parent):
	outGrid = parent.pp2outGB.findChild(QGridLayout)
	inGrid = parent.pp2inGB.findChild(QGridLayout)
	verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding) 
	clearLayout(outGrid)
	clearLayout(inGrid)
	parent.p2inBtns = {}
	parent.p2outBtns = {}
	if parent.pp2typeCB.currentData() == 'in':
		print('in')
		outPins = ['1', '14', '16', '17']
		for i in range(len(outPins)):
			outGrid.addWidget(QLabel(f'Pin {outPins[i]}'), i, 0)
			parent.p2outBtns[f'p2OutPB_{i}'] = QPushButton('Select')
			outGrid.addWidget(parent.p2outBtns[f'p2OutPB_{i}'],i , 1)
		outGrid.addItem(verticalSpacer)

		inPins = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '15']
		for i in range(len(inPins)):
			inGrid.addWidget(QLabel(f'Pin {inPins[i]}'), i, 0)
			parent.p2inBtns[f'p2InPB_{i}'] = QPushButton('Select')
			inGrid.addWidget(parent.p1inBtns[f'p2InPB_{i}'],i , 1)
		inGrid.addItem(verticalSpacer)

	elif parent.pp2typeCB.currentData() == 'out':
		outPins = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '14', '16', '17']
		for i in range(len(outPins)):
			outGrid.addWidget(QLabel(f'Pin {outPins[i]}'), i, 0)
			parent.p2outBtns[f'p2OutPB_{i}'] = QPushButton('Select')
			outGrid.addWidget(parent.p2outBtns[f'p2OutPB_{i}'],i , 1)
		outGrid.addItem(verticalSpacer)

		inPins = ['10', '11', '12', '13', '15']
		for i in range(len(inPins)):
			inGrid.addWidget(QLabel(f'Pin {inPins[i]}'), i, 0)
			parent.p2inBtns[f'p2InPB_{i}'] = QPushButton('Select')
			inGrid.addWidget(parent.p2inBtns[f'p2InPB_{i}'],i , 1)
		inGrid.addItem(verticalSpacer)

	if parent.pp2typeCB.currentData():
		for i in range(len(outPins)):
			button = parent.p2outBtns.get(f'p2OutPB_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			menu.triggered.connect(lambda: utilities.setAxisTabs(parent))
			add_menu(outputs, menu)
			button.setMenu(menu)

		for i in range(len(inPins)):
			button = parent.p2inBtns.get(f'p2InPB_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(inputs, menu)
			button.setMenu(menu)

	"""

	if parent.pp1typeCB.currentData() == 'in':
		outPins = ['1', '14', '16', '17']
		for i in range(len(outPins)):
			outGrid.addWidget(QLabel(f'Pin {outPins[i]}'), i, 0)
			parent.p1outBtns[f'p1OutPB_{i}'] = QPushButton('Select')
			outGrid.addWidget(parent.p1outBtns[f'p1OutPB_{i}'],i , 1)
		outGrid.addItem(verticalSpacer)



		inPins = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '15']
		for i in range(len(inPins)):
			inGrid.addWidget(QLabel(f'Pin {inPins[i]}'), i, 0)
			parent.p1inBtns[f'p1InPB_{i}'] = QPushButton('Select')
			inGrid.addWidget(parent.p1inBtns[f'p1InPB_{i}'],i , 1)
		inGrid.addItem(verticalSpacer)



	if parent.pp1typeCB.currentData() == 'out':
		outPins = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '14', '16', '17']
		for i in range(len(outPins)):
			outGrid.addWidget(QLabel(f'Pin {outPins[i]}'), i, 0)
			parent.p1outBtns[f'p1OutPB_{i}'] = QPushButton('Select')
			outGrid.addWidget(parent.p1outBtns[f'p1OutPB_{i}'],i , 1)
		outGrid.addItem(verticalSpacer)

		for i in range(4):
			button = parent.p1outBtns.get(f'p1OutPB_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)

		inPins = ['10', '11', '12', '13', '15']
		for i in range(len(inPins)):
			inGrid.addWidget(QLabel(f'Pin {inPins[i]}'), i, 0)
			parent.p1inBtns[f'p1InPB_{i}'] = QPushButton('Select')
			inGrid.addWidget(parent.p1inBtns[f'p1InPB_{i}'],i , 1)
		inGrid.addItem(verticalSpacer)

		for i in range(len(inPins)):
			button = parent.p1inBtns.get(f'p1InPB_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(inputs, menu)
			button.setMenu(menu)

	if parent.pp1typeCB.currentData() == 'out':
		print('clear')
	"""

def build(parent):


	"""
	for i in range(11):
		button = getattr(parent, "inputPB_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(inputs, menu)
		button.setMenu(menu)

	for i in range(24):
		button = getattr(parent, "ss7i64in_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(inputs, menu)
		button.setMenu(menu)

	for i in range(24):
		button = getattr(parent, "ss7i69in_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(inputs, menu)
		button.setMenu(menu)

	for i in range(48):
		button = getattr(parent, "ss7i70in_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(inputs, menu)
		button.setMenu(menu)

	for i in range(32):
		button = getattr(parent, "ss7i84in_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(inputs, menu)
		button.setMenu(menu)

	for i in range(6):
		button = getattr(parent, "outputPB_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)

	for i in range(24):
		button = getattr(parent, "ss7i64out_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)

	for i in range(24):
		button = getattr(parent, "ss7i69out_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)

	for i in range(48):
		button = getattr(parent, "ss7i71out_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)

	for i in range(48):
		button = getattr(parent, "ss7i72out_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)

	for i in range(15):
		button = getattr(parent, "ss7i73in_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(inputs, menu)
		button.setMenu(menu)

	for i in range(2):
		button = getattr(parent, "ss7i73out_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)

	for i in range(16):
		button = getattr(parent, "ss7i84out_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)
	"""

def add_menu(data, menu_obj):
	if isinstance(data, dict):
		for k, v in data.items():
			sub_menu = QMenu(k, menu_obj)
			menu_obj.addMenu(sub_menu)
			add_menu(v, sub_menu)
	elif isinstance(data, list):
		for element in data:
			add_menu(element, menu_obj)
	else:
		action = menu_obj.addAction(data)
		action.setIconVisibleInMenu(False)

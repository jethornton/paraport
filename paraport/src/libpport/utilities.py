import os, subprocess
from PyQt5.QtWidgets import QMessageBox, QApplication

def isNumber(s):
	try:
		s[-1].isdigit()
		float(s)
		return True
	except ValueError:
		return False

def axisChanged(parent):
	joint = parent.sender().objectName()[-1]
	axis = parent.sender().currentText()
	if axis in ['X', 'Y', 'Z', 'U', 'V', 'W']:
		getattr(parent, f'axisType_{joint}').setText('LINEAR')
	elif axis in ['A', 'B', 'C']:
		getattr(parent, f'axisType_{joint}').setText('ANGULAR')
	else:
		getattr(parent, f'axisType_{joint}').setText('')
	coordList = []
	for i in range(parent.card['joints']):
		axisLetter = getattr(parent, f'axisCB_{i}').currentText()
		if axisLetter != 'Select':
			coordList.append(axisLetter)
		parent.coordinatesLB.setText(''.join(coordList))
		parent.axes = len(parent.coordinatesLB.text())

def configNameChanged(parent, text):
	if text:
		parent.configNameUnderscored = text.replace(' ','_').lower()
		parent.configPath = os.path.expanduser('~/linuxcnc/configs') + '/' + parent.configNameUnderscored
		parent.pathLabel.setText(parent.configPath)
	else:
		parent.pathLabel.setText('')

def pidSetDefault(parent):
	tab = parent.sender().objectName()[-1]
	if not parent.linearUnitsCB.currentData():
		QMessageBox.warning(parent,'Warning', 'Machine Tab\nLinear Units\nmust be selected', QMessageBox.Ok)
		return
	p = int(1000/(int(parent.servoPeriodSB.cleanText())/1000000))
	getattr(parent, 'p_' + tab).setText(f'{p}')
	getattr(parent, 'i_' + tab).setText('0')
	getattr(parent, 'd_' + tab).setText('0')
	getattr(parent, 'ff0_' + tab).setText('0')
	getattr(parent, 'ff1_' + tab).setText('1')
	getattr(parent, 'ff2_' + tab).setText('0.00013')
	getattr(parent, 'bias_' + tab).setText('0')
	getattr(parent, 'maxOutput_' + tab).setText('0')
	if parent.linearUnitsCB.itemData(parent.linearUnitsCB.currentIndex()) == 'inch':
		maxError = '0.0005'
	else:
		maxError = '0.0127'
	getattr(parent, 'maxError_' + tab).setText(maxError)
	getattr(parent, 'deadband_' + tab).setText('0')

def driveChanged(parent):
	timing = parent.sender().itemData(parent.sender().currentIndex())
	if timing:
		parent.stepTime.setText(timing[0])
		parent.stepSpace.setText(timing[1])
		parent.dirSetup.setText(timing[2])
		parent.dirHold.setText(timing[3])
		parent.stepTime.setEnabled(False)
		parent.stepSpace.setEnabled(False)
		parent.dirSetup.setEnabled(False)
		parent.dirHold.setEnabled(False)
	else:
		parent.stepTime.setEnabled(True)
		parent.stepSpace.setEnabled(True)
		parent.dirSetup.setEnabled(True)
		parent.dirHold.setEnabled(True)

def plcOptions():
	return ['ladderRungsSB', 'ladderBitsSB', 'ladderWordsSB',
	'ladderTimersSB', 'iecTimerSB', 'ladderMonostablesSB', 'ladderCountersSB',
	'ladderInputsSB', 'ladderOutputsSB', 'ladderExpresionsSB',
	'ladderSectionsSB', 'ladderSymbolsSB', 'ladderS32InputsSB',
	'ladderS32OuputsSB', 'ladderFloatInputsSB', 'ladderFloatOutputsSB']

def updateAxisInfo(parent):
	if parent.sender().objectName() == 'actionOpen':
		return
	joint = parent.sender().objectName()[-1]
	scale = getattr(parent, 'scale_' + joint).text()
	if scale and isNumber(scale):
		scale = float(scale)
	else:
		return

	maxVelocity = getattr(parent, 'maxVelocity_' + joint).text()
	if maxVelocity and isNumber(maxVelocity):
		maxVelocity = float(maxVelocity)
	else:
		return

	maxAccel = getattr(parent, 'maxAccel_' + joint).text()
	if maxAccel and isNumber(maxAccel):
		maxAccel = float(maxAccel)
	else:
		return

	if not parent.linearUnitsCB.currentData():
		parent.errorDialog('Machine Tab:\nLinear Units must be selected')
		return
	accelTime = maxVelocity / maxAccel
	getattr(parent, 'timeJoint_' + joint).setText(f'{accelTime:.2f} seconds')
	accelDistance = accelTime * 0.5 * maxVelocity
	getattr(parent, 'distanceJoint_' + joint).setText(f'{accelDistance:.2f} {parent.linearUnitsCB.currentData()}')
	stepRate = scale * maxVelocity
	getattr(parent, 'stepRateJoint_' + joint).setText(f'{abs(stepRate):.0f} pulses')


def spindleTypeChanged(parent): 
	#print(parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()))
	if parent.spindleTypeCB.currentData():
		parent.spindleGB.setEnabled(True)
		parent.spindleInfoGB.setEnabled(True)
		parent.encoderGB.setEnabled(True)
		parent.spindlepidGB.setEnabled(True)
		if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()) == '1':
			parent.spindleInfo1Lbl.setText("PWM on Step 4")
			parent.tb2p3LB.setText("PWM +")
			parent.tb2p2LB.setText("PWM -")
			parent.spindleInfo2Lbl.setText("Direction on Dir 4")
			parent.tb2p5LB.setText("Direction +")
			parent.tb2p4LB.setText("Direction -")
			parent.spindleInfo3Lbl.setText("Select Enable on the Outputs tab")
		if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()) == '2':
			parent.spindleInfo1Lbl.setText("UP on Step 4")
			parent.tb2p3LB.setText("UP +")
			parent.tb2p2LB.setText("UP -")
			parent.spindleInfo2Lbl.setText("Down on Dir 4")
			parent.tb2p5LB.setText("DOWN +")
			parent.tb2p4LB.setText("DOWN -")
			parent.spindleInfo3Lbl.setText("Select Enable on the Outputs tab")
		if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()) == '3':
			parent.spindleInfo1Lbl.setText("PDM on Step 4")
			parent.tb2p3LB.setText("PDM +")
			parent.tb2p2LB.setText("PDM -")
			parent.spindleInfo2Lbl.setText("Direction on Dir 4")
			parent.tb2p5LB.setText("Direction +")
			parent.tb2p4LB.setText("Direction -")
			parent.spindleInfo3Lbl.setText("Select Enable on the Outputs tab")
		if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()) == '4':
			parent.spindleInfo1Lbl.setText("Direction on Step 4")
			parent.tb2p3LB.setText("Direction +")
			parent.tb2p2LB.setText("Direction -")
			parent.spindleInfo2Lbl.setText("PWM on Dir 4")
			parent.tb2p5LB.setText("PWM +")
			parent.tb2p4LB.setText("PWM -")
			parent.spindleInfo3Lbl.setText("Select Enable on the Outputs tab")


def fileNew(parent):
	parent.errorMsgOk('Close the Tool,\n Then open', 'Info!')

def fileSaveAs(parent):
	parent.errorMsgOk('Change the Name,\n Then Save', 'Info!')

def copyOutput(parent):
	qclip = QApplication.clipboard()
	qclip.setText(parent.machinePTE.toPlainText())
	parent.statusbar.showMessage('Output copied to clipboard')

def setupPorts(parent):
	pass

def setAxisTabs(parent):
	for i in range(1,10):
		parent.axisTabs.setTabEnabled(i, False)
	axes = ['X', 'Y', 'Z', 'A', 'B', 'C', 'U', 'V', 'W']
	tabs = {'X':1, 'Y':2, 'Z':3, 'A':4, 'B':5, 'C':6, 'U':7, 'V':8, 'W':9}

	if parent.p1outBtns:
		print('p1outBtns')
		for k, v in parent.p1outBtns.items():
			if v.text().startswith(tuple(axes)):
				parent.axisTabs.setTabEnabled(tabs[v.text()[0]], True)
	if parent.p2outBtns:
		print('p2outBtns')
		for k, v in parent.p2outBtns.items():
			if v.text().startswith(tuple(axes)):
				parent.axisTabs.setTabEnabled(tabs[v.text()[0]], True)



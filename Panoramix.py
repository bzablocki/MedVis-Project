#For this, we need vtk:
import vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy
#ginny

def Panoramix():
  selectedPlane1 = [0,0,0,0]
  selectedPlane2 = [0,0,0,0]

  def updateClippingPlane(obj, event):
    obj.GetCursorData(selectedPlane1)
    print("plane1: ", selectedPlane1)
    # global clippingPlane
    # Write some codes (ref to what you’ve done in step 2) # no more than two lines
    clippingPlane.SetOrigin(obj.GetOrigin()) 
    # clippingPlane.SetNormal(obj.GetNormal())
    clippingPlane.Modified()

  def updateClippingPlane2(obj, event):
    obj.GetCursorData(selectedPlane2)
    print("plane2: ", selectedPlane2)
    # global clippingPlane2
    # Write some codes (ref to what you’ve done in step 2) # no more than two lines
    clippingPlane2.SetOrigin(obj.GetOrigin()) 
    # clippingPlane2.SetNormal(obj.GetNormal())
    clippingPlane2.Modified()

  reader = vtk.vtkXMLImageDataReader()
  reader.SetFileName(r"aneurysm.vti")
  reader.Update()
  data = reader.GetOutput()


  image = vtk.vtkImageMathematics()
  image.SetInput1Data(data);
  image.SetConstantC(1024);
  image.SetOperationToAddConstant();
  image.Update();
  
  output = image.GetOutput();
  
  shifter = vtk.vtkImageShiftScale()
  shifter.SetInputConnection(image.GetOutputPort())
  shifter.SetOutputScalarTypeToUnsignedShort()
  shifter.Update()
  
  shifter2 = vtk.vtkImageShiftScale()
  shifter2.SetInputConnection(image.GetOutputPort())
  shifter2.SetOutputScalarTypeToInt()
  shifter2.Update()

  
  
  otf = vtk.vtkPiecewiseFunction()
  ctf = vtk.vtkColorTransferFunction()
  otf.RemoveAllPoints() 
  otf.AddPoint(image.GetOutput().GetScalarRange()[0]+100, 0.0) 
  otf.AddPoint((image.GetOutput().GetScalarRange()[0]+image.GetOutput().GetScalarRange()[1])/2, 0.3) 
  otf.AddPoint(image.GetOutput().GetScalarRange()[1], 1.0)
  ctf.RemoveAllPoints() 
  ctf.AddRGBPoint(image.GetOutput().GetScalarRange()[0], 1, 1, 0) 
  ctf.AddRGBPoint(1250, 0.65, 0.7, 1.0) 
  ctf.AddRGBPoint(image.GetOutput().GetScalarRange()[1], 0, 0, 1)
  
  propVolume = vtk.vtkVolumeProperty()
  propVolume.ShadeOn()
  propVolume.SetColor(ctf) 
  propVolume.SetScalarOpacity(otf) 
  propVolume.SetInterpolationTypeToLinear()
  
  #rayCast = vtk.vtkVolumeRayCastCompositeFunction() 
  rayCast = vtk.vtkVolumeRayCastIsosurfaceFunction()
  rayCast.SetIsoValue(1200)
  #ayCast.SetCompositeMethodToInterpolateFirst()
  #rayCast.SetCompositeMethodToClassifyFirst()
  
  mapperVolume = vtk.vtkVolumeRayCastMapper() 
  mapperVolume.SetVolumeRayCastFunction(rayCast) 
  mapperVolume.SetInputConnection(shifter.GetOutputPort())
  
  planeWidget = vtk.vtkImagePlaneWidget() 
  planeWidget.SetInputConnection(reader.GetOutputPort()) 
  planeWidget.SetPlaneOrientationToZAxes()
  planeWidget.SetSliceIndex(int(reader.GetOutput().GetDimensions()[2]/2))
  planeWidget.AddObserver("InteractionEvent", updateClippingPlane)
  
  planeWidget2 = vtk.vtkImagePlaneWidget() 
  planeWidget2.SetInputConnection(reader.GetOutputPort()) 
  planeWidget2.SetPlaneOrientationToZAxes()
  planeWidget2.SetSliceIndex(int(reader.GetOutput().GetDimensions()[2]-15.0))
  planeWidget2.AddObserver("InteractionEvent", updateClippingPlane2)
  
  clippingPlane = vtk.vtkPlane()
  clippingPlane.SetOrigin(planeWidget.GetOrigin()) 
  clippingPlane.SetNormal(planeWidget.GetNormal())
  
  clippingPlane2 = vtk.vtkPlane()
  clippingPlane2.SetOrigin(planeWidget2.GetOrigin()) 
  clippingPlane2.SetNormal([0,0,-1])#planeWidget2.GetNormal())
  
  # mapperVolume.AddClippingPlane(clippingPlane)
  # mapperVolume.AddClippingPlane(clippingPlane2)

  # plane1:  [79.0, 86.0, 59.0, 403.0]
  # plane2:  [123.0, 74.0, 104.0, 334.0]

  pointOnPlane1 = [79.0, 86.0, 59.0, 403.0]
  pointOnPlane2 = [123.0, 74.0, 104.0, 334.0]

  # output = reader.GetOutput()
  # points = output.GetPoints()
  # array = output.GetData()
  # numpy_nodes = vtk_to_numpy(image.GetOutput().GetPointData())
  # print(numpy_nodes.shape)
  # print(output.GetNumberOfPoints())
  
  gtf = vtk.vtkPiecewiseFunction()
  gtf.RemoveAllPoints() 
  gtf.AddPoint(image.GetOutput().GetScalarRange()[0], 0.0) 
  gtf.AddPoint((image .GetOutput().GetScalarRange()[0]+ image.GetOutput().GetScalarRange()[1])/2, 0.8) 
  gtf.AddPoint(image.GetOutput().GetScalarRange()[1], 1.0)
  propVolume.SetGradientOpacity(gtf)
  
  actorVolume = vtk.vtkVolume()
  actorVolume.SetMapper(mapperVolume)
  actorVolume.SetProperty(propVolume)


  renderWindow = vtk.vtkRenderWindow()
  renderer = vtk.vtkRenderer()
  renderWindow.AddRenderer(renderer)
  renderer.AddActor(actorVolume)
  # renderer.SetBackground(1, 1, 1); 

  iren = vtk.vtkRenderWindowInteractor()
  iren.SetRenderWindow(renderWindow)
  iren.Initialize()
  
  planeWidget.SetInteractor(iren)#render window interactor planeWidget.PlaceWidget()
  planeWidget.On() # enable the interaction
  
  planeWidget2.SetInteractor(iren)#render window interactor planeWidget.PlaceWidget()
  planeWidget2.On() # enable the interaction
  
  
  
  renderWindow.Render()
  
  iren.Start()
  
 # Make interactive via callback function
  


  # reader.Update()
  
  # data = reader.GetOutput()  
  # data_range = data.GetScalarRange()
  # print("data_range", data_range)
  
  # imagemath = vtk.vtkImageMathematics()
  # imagemath.SetInputConnection(reader.GetOutputPort())
  # imagemath.SetConstantC(1024.0)
  # imagemath.SetOperationToAddConstant()
  # imagemath.Update()
  
  # data = imagemath.GetOutput()
  # data_range = data.GetScalarRange()
  # print("data_range", data_range)
  
  # #Contour
  # #contour = vtk.vtkContourFilter()
  # #contour.SetInputConnection(imagemath.GetOutputPort())
  # #contour.SetValue(0, 2000)
  # #contour.SetValue(1, 800)
  # #contour.GenerateValues(3,1400, 2000)
  
  # otf = vtk.vtkPiecewiseFunction()
  # ctf = vtk.vtkColorTransferFunction()
  
  # otf.RemoveAllPoints()
  # otf.AddPoint(imagemath.GetOutput().GetScalarRange()[0]+100, 0.0)
  # otf.AddPoint((imagemath.GetOutput().GetScalarRange()[0]+imagemath.GetOutput().GetScalarRange()[1])/2, 0.3)
  # otf.AddPoint(imagemath.GetOutput().GetScalarRange()[1], 1.0)
  # ctf.RemoveAllPoints()
  # ctf.AddRGBPoint(imagemath.GetOutput().GetScalarRange()[0], 1, 1, 0)
  # ctf.AddRGBPoint(1250, 0.65, 0.7, 1.0)
  # ctf.AddRGBPoint(imagemath.GetOutput().GetScalarRange()[1], 0, 0, 1)
  
  # propVolume = vtk.vtkVolumeProperty()
  # propVolume.ShadeOn()
  # propVolume.SetColor(ctf)
  # propVolume.SetScalarOpacity(otf)
  # propVolume.SetInterpolationTypeToLinear()
  
  # #rayCast = vtk.vtkVolumeRayCastMIPFunction()
  
  # rayCast = vtk.vtkVolumeRayCastIsosurfaceFunction()
  # rayCast.SetIsoValue(1200)
  
  # #rayCast = vtk.vtkVolumeRayCastCompositeFunction()
  # #rayCast.SetCompositeMethodToInterpolateFirst()
  # #rayCast.SetCompositeMethodToClassifyFirst()
  
  
    
  # #We will need a mapper and an actor, let`s use the vtkPolyDataMapper and the vtkActor classes.
  # #mapper = vtk.vtkPolyDataMapper()
  # #mapper.SetInputConnection(contour.GetOutputPort())
  # #mapper.ScalarVisibilityOff()
  
  # shift = vtk.vtkImageShiftScale()
  # shift.SetInputConnection(imagemath.GetOutputPort())
  # shift.SetOutputScalarTypeToUnsignedShort()
  
  # mapperVolume = vtk.vtkVolumeRayCastMapper()
  # mapperVolume.SetVolumeRayCastFunction(rayCast)
  # mapperVolume.SetInputConnection(shift.GetOutputPort())
  
  # actorVolume = vtk.vtkVolume()
  # actorVolume.SetMapper(mapperVolume)
  # actorVolume.SetProperty(propVolume)
  
  # gtf = vtk.vtkPiecewiseFunction()
  # gtf.RemoveAllPoints()
  # gtf.AddPoint(imagemath.GetOutput().GetScalarRange()[0], 0.0)
  # gtf.AddPoint((imagemath .GetOutput().GetScalarRange()[0]+ imagemath.GetOutput().GetScalarRange()[1])/2, 0.8)
  # gtf.AddPoint(imagemath.GetOutput().GetScalarRange()[1], 1.0)
  # propVolume.SetGradientOpacity(gtf)
  
  
 
  # # Define FIRST plane and clipping Plane
  # planeWidget = vtk.vtkImagePlaneWidget()
  # planeWidget.SetInputConnection(reader.GetOutputPort())
  # planeWidget.SetPlaneOrientationToZAxes()
  # #print("slice pos", planeWidget.GetSlicePosition())
  # #print("go to ", planeWidget.GetSlicePosition()+410.0)
  # #planeWidget.SetOrigin([-192.00000375, -318.00000375, -300.5])
  # #print("slice pos", planeWidget.GetSlicePosition())
  # #planeWidget.SetSliceIndex(0) #int(reader.GetOutput().GetDimensions()[2]/2))
  
  # clippingPlane = vtk.vtkPlane()
  # # print(planeWidget.GetOrigin())
  # #clippingPlane.SetOrigin(planeWidget.GetOrigin())
  # origin = [-192.00000375, -318.00000375, -300.5]
  # clippingPlane.SetOrigin(origin)
  # normal = [planeWidget.GetNormal()[0],planeWidget.GetNormal()[1],planeWidget.GetNormal()[2]]
  # print("normal", normal)
  # clippingPlane.SetNormal(normal)
  
  # def updateClippingPlane(obj, event):
  #   print(obj.GetCurrentImageValue())
  #   #clippingPlane.SetOrigin(obj.GetOrigin())
  #   #lippingPlane.Modified()
    
  # planeWidget.AddObserver("InteractionEvent", updateClippingPlane)
  
  
  # # Define SECOND plane and clipping Plane
  # ## planeWidget2 = vtk.vtkImagePlaneWidget()
  # ## planeWidget2.SetInputConnection(reader.GetOutputPort())
  # ## planeWidget2.SetPlaneOrientationToZAxes()
  # ## planeWidget2.SetSliceIndex(int(reader.GetOutput().GetDimensions()[2]))
  
  # ## print("normal:", planeWidget2.GetNormal())  
  # ## clippingPlane2 = vtk.vtkPlane()
  # ## clippingPlane2.SetOrigin(planeWidget2.GetOrigin())
  # ## normal = [planeWidget2.GetNormal()[0],planeWidget2.GetNormal()[1],-planeWidget2.GetNormal()[2]]
  # ## print("normal mod:", normal)
  # ## clippingPlane2.SetNormal(normal)
  
  # ## def updateClippingPlane2(obj, event):
  # ##   clippingPlane2.SetOrigin(obj.GetOrigin())
  # ##   clippingPlane2.Modified()
    
  # #planeWidget2.AddObserver("InteractionEvent", updateClippingPlane2)
  
  
  # # Add planes to Mapper
  # planes = vtk.vtkPlaneCollection()
  # planes.AddItem(clippingPlane)
  # ## planes.AddItem(clippingPlane2)
  # mapperVolume.SetClippingPlanes(planes)
  
  
  # #Let`s add our render window and an interactor:
  # renderWindow = vtk.vtkRenderWindow()
  # renderer = vtk.vtkRenderer()

  # renderWindow.AddRenderer(renderer)
  # renderer.AddActor(actorVolume)
  
  # iren = vtk.vtkRenderWindowInteractor()
  
 
  # iren.SetRenderWindow(renderWindow)
  # iren.Initialize()
  
  # ## planeWidget2.SetInteractor(iren)# render window interactor
  # ## planeWidget2.PlaceWidget()
  # ## planeWidget2.On() # enable the interaction
  
  # planeWidget.SetInteractor(iren)# render window interactor
  # planeWidget.PlaceWidget()
  # planeWidget.On() # enable the interaction
  
  
  
  # renderWindow.Render()
  # iren.Start()
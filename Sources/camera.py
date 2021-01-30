from pypylon import pylon
import numpy as np

class Camera(pylon.InstantCamera):
    def __init__(self, PipeEnd, Alive):
        super().__init__(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        self.pipe = PipeEnd
        self.Alive = Alive
        self.settings()
        self.CameraLoop()

    def settings(self):
        self.MaxNumBuffer = 5
        self.ExposureAuto.SetValue('Off')
        self.ExposureTimeAbs = 100
        self.UserSetSelector = "UserSet1"
        self.UserSetSave.Execute()
        self.UserSetDefaultSelector = "UserSet1"
        self.GainAuto.SetValue('Once')
        self.AcquisitionMode.SetValue('Continuous')
        self.TriggerSelector.SetValue('FrameStart')
        self.TriggerMode.SetValue('On')
        self.TriggerSource.SetValue('Software')
        self.PixelFormat.SetValue('Mono8')

    def CameraLoop(self):
        self.Open()
        self.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
        if self.IsOpen():
            while self.Alive:
                if self.WaitForFrameTriggerReady(10000):
                    self.ExecuteSoftwareTrigger()
                if self.GetGrabResultWaitObject().Wait(0):
                    grabResult = self.RetrieveResult(50)
                    if grabResult.GrabSucceeded():
                        image = self.converter.Convert(grabResult)
                        self.pipe.send(image.GetArray())
                    else:
                        print('skipped frame')
            grabResult.Release()
        self.StopGrabbing()
        self.Release()
from Box2D import (b2RayCastCallback)    

# Define a callback for the ray cast
class RayCastCallback(b2RayCastCallback):
    def __init__(self):
        b2RayCastCallback.__init__(self)
        self.hit = False

    def ReportFixture(self, fixture, point, normal, fraction):
        self.hit = True if fixture.body.userData == 'blocker' else self.hit 

        return 0 if self.hit else 1
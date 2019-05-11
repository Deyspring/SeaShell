import math

#import sys
#sys.path.append('/Users/katherinedey/Documents/SeashellGenerator/class_shell/')
#print(sys.executable)


from shellPresets import BoatEarMoon

#4/30 last touched
# Cannot import presets from shellPresets file
# problem with nodules calculations
# Figure out defaults for n, m, turns, s and i , shell defaults without these end up being strange. 
# Check that original values for various shell forms are correct. 

class Shell: 


    def __init__(self, n, m, turns, s, i, D, alpha_, beta, phi, mu, omega, A, a, b, L, P, W1, W2, N ):
        self.n = n            # Resolution of spiral
        self.m = m            # Resolution of spline
        self.turns = turns    # Number of turns of spiral
        self.s = s            # Angle from b to a axis in spiral 
                              # changing s to -1 makes spline larger, but -50 or 50 changes nothing. sin effect I think. 
        self.i = i            # Clipping? of spiral? 
                              # values of less than one show no change, values of 10+ clip spiral into shorter coils. At 50, the spiral disappears. The spline does not change. 
                              # Changing j values shows a similar effect. 
        
        self.D = D            # Direction of coiling, 1 dextral, -1 sistral 
        self.alpha_ = alpha_  # Equiangular angle of spiral 
        self.beta = beta      # Enlarging angle of spiral, breadth
        self.phi = phi        # Spline rotation about spiral point
        self.mu = mu          # Spline rotation about spiral point
        self.omega = omega    # Spline rotation about spiral point
        self.A = A            # Size of spiral aperture
        self.a = a            # Minor spline length
        self.b = b            # Major spline length
        self.L = L            # Height of nodule
        self.P = P            # Angle of nodule in regards to spline
        self.W1 = W1          # Length of nodule in regards to spline
        self.W2 = W2          # Length of nodule along spiral 
        self.N = N            # Number of nodules along a complete revolution of theta. 


    def generateShell(self):  
        """Generate the main spiral."""
        shell_matrix =[]
        spiral_matrix =[]
        while self.i < self.n: 
            theta = float(map(self.i, 0, self.n, 0, self.turns))
            rad =   float(exp(theta * cos(self.alpha_) / sin(self.alpha_)) )
            
            x = float (self.A  * rad * sin(self.beta) * cos(theta) * self.D)
            y = float (self.A  * rad * sin(self.beta) * sin(theta))
            z = float (-self.A * rad * cos(self.beta))
            
            spiral_i = PVector(x,y,z)
            spiral_matrix.append(spiral_i) 
            
            #Initialization values for generateSpline.
            self.j = 0
            spline_matrix =[]
            
            def generateSpline(x,y,z):
                """Generate spline around each spiral point. Values from generateSpiral are passed to this nested function."""
                while self.j < self.m: 
                    s = float(map(self.j, 0, self.m, 0, TWO_PI)) 
                    r2 = float(pow( pow(cos(s)/self.a,2) + pow(sin(s)/self.b,2), -0.5 ))
                    surfrad = float(0)
                    
                    #Add shell surface nodules and manipulations.
                    if (self.W1==0 or self.W2==0 or self.N==0):
                        surfrad = 0
                    else: 
                        lt = float((TWO_PI / self.N) * ( self.N*theta / TWO_PI - int(self.N*theta / TWO_PI) ))
                        surfrad = self.L * exp( -( pow(2*(s-self.P)/self.W1, 2) + pow(2*lt/self.W2, 2) ) ) 
                    
                    r2 += surfrad # += means add r2 to surfrad
                    
                    #Generate spline point. 
                    x = cos(s + self.phi) * cos(theta + self.omega) * r2 * rad * self.D  # This line closes the opening of the curve at the origin
                    y = cos(s + self.phi) * sin(theta + self.omega) * r2 * rad
                    z = sin(s + self.phi)                           * r2 * rad
                    
                    #Adjust orientation of the point so spline does not flatten against the spiral curve.
                    x -= sin(self.mu) * sin(s + self.phi) * sin(theta + self.omega) * r2
                    y += sin(self.mu) * sin(s + self.phi) * cos(theta + self.omega) * r2
                    z *= cos(self.mu)
                    
                    spline_point = PVector(x,y,z)
                    
                    spline_point_adjusted = map(sum, zip(spiral_i, spline_point))
                    spline_matrix.append(spline_point_adjusted) 
                    self.j = self.j+ 1 
                return spline_matrix
            
            #Call generateSpline from within generateSpiral
            spline = generateSpline(*spiral_i)
            #Append returned spline_matrix to shell_matrix
            shell_matrix.append(spline) # shell_matrix should be of form: ([[xyz],[xyz],[xyz]],[[x,y,z],[x,y,z],[x,y,z]]) etc. 
            #print ("shell_matrix", shell_matrix) 
            self.i = self.i + 1  
            
        return shell_matrix
            




#######################################################

def PreciousWentleTrap():
    """Variables for the creation of a Precious Wentle Trap Shell"""
    D = 1
    alpha_=math.radians(86) 
    beta =math.radians(10) 
    phi=math.radians(-45) 
    mu=math.radians(5) 
    omega=math.radians(1) 
    A=90
    a=20
    b=20
    L=14
    P=40
    W1=180
    W2=0.4
    N=100
    return D, alpha_, beta, phi, mu, omega, A, a, b, L, P, W1, W2, N
    

currentFrame = 0

def setup():
  size(600,600,P3D) 
  frameRate(24)

def draw():
  background(255,255,255)
  global currentFrame
  currentFrame = currentFrame + 1
  
  fov =  float(PI/3)
  cameraZ = float((height/2.0) / tan(fov/2.0))
  perspective(fov, float(width)/float(height), cameraZ/10.0, cameraZ*10.0) 
  
  translate(300,300)
  rotateY(currentFrame/24.0)
 # n, m, turns, s, i 
  test = Shell(20,10,10,10,0,*PreciousWentleTrap()) # Use * to unpack tuples
  shell_points = test.generateShell()

  for item in shell_points: 
        for vertex in item: 
            stroke(0,0,255)
            strokeWeight(10)
            point(*vertex)


            
                    

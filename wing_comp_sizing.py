import math

def spar_str_sizing(N,W_cent,sigma_max,tau_max,b,h,taper):
    A_cap = N*W_cent*b*(1+2*taper)/(12*sigma_max*h*(1+taper))
    A_web = N*W_cent/(2*tau_max)
    return A_cap,A_web
def spar_stiff_sizing(N,W_cent,E,b,h,tip_def,taper,):
    A_cap= N*W_cent*b**2*(1+2*taper)/(48*E*h**2*tip_def*(1+taper))
    return A_cap


def skin_str_sizing(tau_max,q_ne,b_ail,c_ail,cm,A_y): #assumes A_y is vector of enclised area as function of span_loc
    t_y= q_ne*b_ail*c_ail**2*cm/(2*A_y*tau_max)
    return t_y

def skin_stiff_sizing(q_ne,b_ail,c_ail,y_ail,cm,stot,A,G,def_max):
    t = q_ne*b_ail*c_ail**2*y_ail*cm*stot/(4*A**2*G*def_max)
    return t

#pulltruded carbon caps
E_carbon=138*10**9
sigma_carbon=1.72*10**9
rho_carbon = 1623.63194143383

#2 oz glass materials
t_per_ply=0.0035*0.00254 #m
G_glass = 30*10**9 #shear modulus
tau_glass = 40*10**6
rho_glass = 767.813267813*2 #accounts for additional weight of 1:1 resin to fabric


def get_sizing(N,W_cent,sigma_max,tau_max,b,h,taper,tip_def,E,q_ne,b_ail,c_ail,y_ail,A,G,def_max,stot,cm):
    A_cap_str,A_web = spar_str_sizing(N,W_cent,sigma_max,tau_max,b,h,taper)
    A_cap_stiff = spar_stiff_sizing(N,W_cent,E,b,h,tip_def,taper)
    t_skin = skin_stiff_sizing(q_ne,b_ail,c_ail,y_ail,cm,stot,A,G,def_max)
    return max(A_cap_stiff,A_cap_str),A_web,t_skin

# N = 20
# W_cent = 4.7*9.81 #N 
# b = 3.825
# h = 0.09*0.420
# taper = 0.824571429
# q_ne = 0.5*1.225*(1.3*9.38)**2 #30%overspeed
# tip_def= b/2*math.cos(6*math.pi/180)
# b_ail = 0.25*b
# c_ail = 0.2*0.310
# y_ail = 0.333*b
# A = 0.062*0.365*0.365
# def_max = 2*math.pi/180
# stot = 2.3*0.365
# cm = 0.4
N = input("Enter load factor (safety factor * expected load factor")
W_cent = input("Enter aircraft mass (minus wing) (for tail surfaces enter desired max torque/tail boom length)")
b = input("Enter span")
h = input("Enter wing max thickness")
taper = input("Enter taper")
q_ne = input("Enter max q ")
tip_def = input("Enter max tip deflection allowed")
b_ail = input("Enter control surface span")
c_ail = input("Enter control surface chord")
y_ail = input("distance from root to center of control surface")
A = input("Enter average cross sectional area")
def_max = input("Enter maximum tip twist allowed")
stot = input("Enter total surface area")
cm = input("Enter maximum CM")
A_cap,A_web,t_skin = get_sizing(N,W_cent,sigma_carbon,tau_glass,b,h,taper,tip_def,E_carbon,q_ne,b_ail,c_ail,y_ail,A,G_glass,def_max,stot,cm)
mass_cap = A_cap*b*rho_carbon*2
mass_web = A_web*b*rho_glass
mass_skin = t_skin*stot*b*rho_glass


web_plies = A_web/(4*h*t_per_ply)
skin_plies = t_skin/t_per_ply
web_plies = math.ceil(web_plies)
skin_plies = math.ceil(skin_plies)
A_web = (4*h*t_per_ply)*web_plies
t_skin = t_per_ply*skin_plies
mass_web = A_web*b*rho_glass
mass_skin = t_skin*stot*b*rho_glass
foam_mass = 0.7881*25.5/32 #kg
balsa_mass = 3.825*(h**2)*150 #kg

joiner_mass = 0.111 #kg
n_joints = 2

all_up_mass = (n_joints*joiner_mass) + foam_mass + balsa_mass + mass_cap + mass_web + mass_skin
mass_defecit = 2.6 - all_up_mass

print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("%%%%%     Composite Areas & plies          %%%%%%")
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("Cap Area: " + str(A_cap) + "m^2")
print("Web Area: " + str(A_web) + "m^2")
print("Web plies: " + str(web_plies))
print("Skin thickness " + str(t_skin) + "m")
print("Skin plies: " + str(skin_plies))

print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("%%%%%           Weight buildup             %%%%%%")
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("Foam weight: " + str(foam_mass) + "kg")
print("Balsa weight: " + str(balsa_mass) + "kg")
print("Joiners weight: " + str(joiner_mass*n_joints) + "kg")
print("Skin weight: " + str(mass_skin) + "kg")
print("Cap weight: " + str(mass_cap) + "kg")
print("Web weight: " + str(mass_web) +  "kg" )
print("All up wing mass: " + str(all_up_mass) + "kg")
print("Mass defecit: " + str(mass_defecit) + "kg")


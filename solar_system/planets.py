from planet import Planet

# One astronomical unit in m
AU = 1.495978707E11

sun = Planet(None, r=4*1.392E9, color='y', mu=1.32712440018E20, name='Sun')

mercury = Planet(sun, a=0.3871*AU, e=0.20564, i=7.006, o=48.34, w=77.46, r=4.879E6,
                 mu=2.2032E13, v0=232.0074961172836, color='k', name='Mercury')

venus = Planet(sun, a=0.7233*AU, e=0.00676, i=3.398, o=76.67, w=131.77, r=1.2104E7,
               mu=3.24859E14, v0=181.98, color='y', name='Venus')

earth = Planet(sun, a=1*AU, e=0.01671022, i=0.00005, o=0., w=102.93, r=1.2742E7,
               mu=3.986004418E14, v0=102.34771894896745, color='b', name='Earth')

mars = Planet(sun, a=1.5237*AU, e=0.09337, i=1.852, o=49.71, w=336.08, r=6.779E6,
              mu=4.282837E13, v0=354.4672762120501, color='r', name='Mars')

jupiter = Planet(sun, a=5.2025*AU, e=0.04854, i=1.299, o=100.29, w=14.27, r=1.3982E8,
                 mu=1.26686534E17, v0=34.33, color='y', name='Jupiter')

saturn = Planet(sun, a=9.5415*AU, e=0.05551, i=2.494, o=113.64, w=92.86, r=1.1646E8,
                mu=3.7931187E16, v0=50.08, color='y', name='Saturn')

uranus = Planet(sun, a=19.188*AU, e=0.04686, i=0.773, o=73.96, w=172.43, r=5.0724E7,
                mu=5.793939E15, v0=314.20, color='b', name='Uranus')

neptune = Planet(sun, a=30.070*AU, e=0.00895, i=1.770, o=131.79, w=46.68, r=4.9244E7,
                 mu=6.836529E15, v0=304.22, color='b', name='Neptune')

moon = Planet(earth, a=3.8844E8, e=0.0549, i=5.145, o=0, w=0, r=1.7374E6,
              mu=4.9028695E12, v0=0., color='grey', name='Moon')

import turtle

win = turtle.Screen()
win.title('Звёздное небо')
win.setup(800,800)
win.bgcolor('black')
t = turtle.Turtle()
t.hideturtle()

def draw_stars(name, light, stars, x, y):
    t.pensize(1)
    t.penup()
    t.goto(x, y)
    t.pendown()

    t.pencolor('Dark blue')
    t.dot(5,'yellow')


    for star in stars:
        angl = star[0]
        width = star[1]
        t.setheading(angl)
        t.forward(width)
        t.dot(star[2], 'yellow')
        if len(star)==4 and star[3]==0:
            t.penup()
            t.goto(0,0)
            t.pendown()
        elif len(star)==4 and star[3]==1:
            t.penup()
            t.goto(0, 0)
            t.pendown()

    t.penup()
    t.goto(-300,350)
    t.pendown()
    t.pencolor('yellow')
    t.write('Созвездие '+name+'. Яркая звезда - '+light,
                    font=('Arial', 12))

# draw_stars('Лебедь','Денеб', stars_1)
stars =[]

stars_1 = [(-163.01, 75.29, 8, 0),
         (-59.88, 93.65, 3),(-86.91, 74.11 ,4),(-115.39, 65.31,3, 0),
         (112.58, 109.38, 3),(157.98, 96.01, 4),(137.29, 35.38, 3, 0),
         (29.17, 98.49, 4),(19.29, 127.14, 4, 0)]
stars.append((stars_1, 'Лебедь','Денеб', 0, 0))

stars_2 = [(169.71, 55.9, 4),
           (144.46, 43.01, 4),
           (149.42, 25.55, 5),
           (112.25, 23.77, 4),
           (-38.66, 25.61, 3),
           (-59.04, 17.49, 4)]
stars.append((stars_2, 'Ящерица','-', 0, 0))

stars_3 =[( 115.36, 212.47, 6),
          (99.21, 37.48, 4, 0),
          ( -20.58, 176.26,4, 0),
          (-122.29, 192.82,  5, 0),
          (-178, 143.09,  6),
          ( 102.72, 31.78, 3),
          (-69.78, 40.5, 5)]

stars.append((stars_3, 'Орел','Альтаир', 0, 0))

curren_star = 0

def click_btn(x, y):
    global  curren_star
    t.clear()
    print(curren_star, len(stars) )
    if curren_star+1 < len(stars):
        curren_star = curren_star +1
    else:
        curren_star = 0
    star = stars[curren_star]
    draw_stars(star[1],star[2], star[0], star[3], star[4])


star = stars[curren_star]
draw_stars(star[1],star[2], star[0], star[3], star[4])

win.onclick(click_btn, 1)

win.mainloop()

import json
import pickle
from sklearn.linear_model import LogisticRegression

# Load data
with open('movie_data_competition.json') as movie_data_file:
    movie_data = json.load(movie_data_file)

n_movies = len(movie_data)

# Initialize helper lists for binary features
all_ratings = ['G', 'NC17', 'PG', 'PG-13', 'R']
all_genres = ['Action & Adventure', 'Animation', 'Anime & Manga', 'Art House & International', 'Classics', 'Comedy', 'Cult Movies', 'Documentary', 'Drama', 'Faith & Spirituality', 'Gay & Lesbian', 'Horror', 'Kids & Family', 'Musical & Performing Arts', 'Mystery & Suspense', 'Romance', 'Science Fiction & Fantasy', 'Special Interest', 'Sports & Fitness', 'Television', 'Western']
famous_directors = ['Alejandro González Iñárritu', 'Alfonso Cuarón', 'Brian de Palma', 'Chistohper Nolan', 'Clint Eastwood', 'Danny Boyle', 'David Fincher', 'David Lynch', 'Francis Ford Coppola', 'George Lucas', 'Guillermo del Toro', 'Hayao Miyazaki', 'James Cameron', 'Joel Cohen', 'M. Night Shyamalan', 'Martin Scorsese', 'Oliver Stone', 'Paul Thomas Anderson', 'Peter Jackson', 'Quentin Tarantino', 'Ridley Scott', 'Roman Polanski', 'Steven Spielberg', 'Tim Burton', 'Werner Herzog', 'Wes Anderson', 'Woody Allen', 'Zack Snyder']
famous_actors = ['Adam Sandler', 'Adrien Brody', 'Agnes Moorehead', 'Al Pacino', 'Alan Rickman', 'Alec Baldwin', 'Alec Guinness', 'Alicia Silverstone', 'Allison Janney', 'Amanda Seyfried', 'Amber Heard', 'Amy Adams', 'Andy García', 'Angela Bassett', 'Angela Lansbury', 'Angelina Jolie', 'Anjelica Huston', 'Anna Kendrick', 'Anne Bancroft', 'Anne Baxter', 'Anne Hathaway', 'Annette Bening', 'Anthony Hopkins', 'Anthony Perkins', 'Anthony Quinn', 'Antonio Banderas', 'Ashley Greene', 'Ashley Judd', 'Audrey Hepburn', 'Ava Gardner', 'Barbara Stanwyck', 'Barbra Streisand', 'Ben Affleck', 'Ben Kingsley', 'Ben Stiller', 'Benedict Cumberbatch', 'Benicio del Toro', 'Bette Davis', 'Bette Midler', 'Bill Maher', 'Bill Murray', 'Brad Pitt', 'Bradley Cooper', 'Bridget Bardot', 'Brittany Murphy', 'Bruce Willis', 'Bryan Cranston', 'Burt Lancaster', 'Caitlyn Jenner', 'Cameron Diaz', 'Carole Lombard', 'Carrie Fisher', 'Cary Grant', 'Cate Blanchett', 'Catherine Deneuve', "Catherine O'Hara", 'Catherine Zeta-Jones', 'Charles Bronson', 'Charles Laughton', 'Charlie Chaplin', 'Charlie Sheen', 'Charlize Theron', 'Charlton Heston', 'Chelsea Handler', 'Cher', 'Chris Elliott', 'Chris Rock', 'Christian Bale', 'Christina Ricci', 'Christoph Waltz', 'Christopher Lee', 'Christopher Lloyd', 'Christopher Plummer', 'Christopher Walken', 'Cicely Tyson', 'Claire Danes', 'Clark Gable', 'Claudette Colbert', 'Clint Eastwood', 'Cloris Leachman', 'Colin Farrell', 'Colin Firth', 'Dakota Fanning', 'Dan Aykroyd', 'Daniel Craig', 'Daniel Day-Lewis', 'Danny DeVito', 'Danny Glover', 'David Niven', 'Debbie Reynolds', 'Deborah Kerr', 'Debra Winger', 'Dennis Hopper', 'Denzel Washington', 'Diane Keaton', 'Diane Kruger', 'Diane Lane', 'Dianne Wiest', 'Don Cheadle', 'Donald Sutherland', 'Donna Reed', 'Doris Day', 'Drew Barrymore', 'Dustin Hoffman', 'Ed Harris', 'Eddie Murphy', 'Edward G. Robinson', 'Edward Norton', 'Eli Wallach', 'Elisabeth Shue', 'Elizabeth Banks', 'Elizabeth Montgomery', 'Elizabeth Taylor', 'Ellen Burstyn', 'Ellen Page', 'Emily Blunt', 'Eminem', 'Emma Roberts', 'Emma Stone', 'Emma Thompson', 'Emma Watson', 'Errol Flynn', 'Eva Green', 'Eva Longoria', 'Eva Marie Saint', 'Ewan McGregor', 'Faye Dunaway', 'Forest Whitaker', 'Fran Drescher', 'Frances McDormand', 'Fred Astaire', 'Gary Cooper', 'Gary Oldman', 'Gary Sinise', 'Geena Davis', 'Gena Rowlands', 'Gene Hackman', 'Gene Kelly', 'Gene Tierney', 'Gene Wilder', 'Geoffrey Rush', 'George C. Scott', 'George Clooney', 'Gerard Butler', 'Ginger Rogers', 'Glenn Close', 'Glenn Ford', 'Gloria Swanson', 'Goldie Hawn', 'Grace Kelly', 'Greer Garson', 'Gregory Peck', 'Greta Garbo', 'Gwyneth Paltrow', 'Halle Berry', 'Harrison Ford', 'Harvey Keitel', 'Hattie McDaniel', 'Heath Ledger', 'Hedy Lamarr', 'Helen Hunt', 'Helen Mirren', 'Helena Bonham Carter', 'Henry Fonda', 'Hilary Swank', 'Holly Hunter', 'Hugh Jackman', 'Hugh Laurie', 'Humphrey Bogart', 'Ian McKellen', 'Ingrid Bergman', 'Irene Dunne', 'Isabella Rossellini', 'Jack Lemmon', 'Jack Nicholson', 'Jada Pinkett Smith', 'Jake Gyllenhaal', 'James Caan', 'James Cagney', 'James Coburn', 'James Dean', 'James Earl Jones', 'James Franco', 'James Garner', 'James McAvoy', 'James Stewart', 'James Woods', 'Jamie Lee Curtis', 'Jane Fonda', 'Jane Wyman', 'Janet Leigh', 'Jason Biggs', 'Jason Robards Jr.', 'Jason Schwartzman', 'Jason Statham', 'Javier Bardem', 'Jean Arthur', 'Jean Harlow', 'Jean Reno', 'Jean Simmons', 'Jean-Claude Van Damme', 'Jeff Bridges', 'Jeff Goldblum', 'Jennifer Aniston', 'Jennifer Connelly', 'Jennifer Garner', 'Jennifer Lawrence', 'Jennifer Lopez', 'Jeremy Irons', 'Jesse Eisenber', 'Jessica Biel', 'Jessica Chastain', 'Jessica Lange', 'Jessica Szohr', 'Jessica Tandy', 'Jim Carrey', 'Jim Caviezel', 'Jimmy Fallon', 'Joan Crawford', 'Joan Cusack', 'Joan Fontaine', 'Joan Plowright', 'Joanne Woodward', 'Joaquin Phoenix', 'Jodie Foster', 'Joe Pesci', 'John Cleese', 'John Cusack', 'John Goodman', 'John Hurt', 'John Malkovich', 'John Travolta', 'John Wayne', 'Johnny Depp', 'Jon Voight', 'Jonah Hill', 'Joseph Gordon-Levitt', 'Joy Behar', 'Jude Law', 'Judi Dench', 'Judy Garland', 'Julia Roberts', 'Julia Stiles', 'Julianne Moore', 'Julie Andrews', 'Julie Christie', 'Julie Walters', 'Juliette Binoche', 'Juliette Lewis', 'Kanye West', 'Kate Beckinsale', 'Kate Hudson', 'Kate Winslet', 'Katherine Hepburn', 'Kathleen Turner', 'Kathy Bates', 'Katie Cassidy', 'Keanu Reeves', 'Keira Knightley', 'Kenneth Branagh', 'Kevin Bacon', 'Kevin Costner', 'Kevin Kline', 'Kevin Spacey', 'Khloé Kardashian', 'Kiefer Sutherland', 'Kim Basinger', 'Kim Novak', 'Kirk Douglas', 'Kirsten Dunst', 'Kristen Bell', 'Kristen Stewart', 'Kristin Scott Thomas', 'Kurt Russell', 'Lana Turner', 'Laura Dern', 'Laura Linney', 'Lauren Bacall', 'Laurence Fishburne', 'Laurence Olivier', 'Lea Michele', 'Lee Marvin', 'Lee Van Cleef', 'Leonardo DiCaprio', 'Leslie Nielsen', 'Liam Neeson', 'Lily Tomlin', 'Lindsay Lohan', 'Liv Tyler', 'Loretta Young', 'Lucille Ball', "Lupita Nyong'o", 'Madeleine Stowe', 'Madeline Kahn', 'Madonna', 'Mae West', 'Maggie Gyllenhaal', 'Maggie Smith', 'Marilyn Monroe', 'Marion Cotillard', 'Marisa Tomei', 'Mark Ruffalo', 'Mark Wahlberg', 'Marlene Dietrich', 'Marlon Brando', 'Martin Sheen', 'Mary McDonnell', 'Mary Steenburgen', 'Mary Tyler Moore', 'Mary-Louise Parker', 'Matt Damon', 'Matthew McConaughey', "Maureen O'Hara", 'Max von Sydow', 'Meg Ryan', 'Mel Gibson', 'Melanie Griffith', 'Melissa McCarthy', 'Meryl Streep', 'Michael Caine', 'Michael Cera', 'Michael Clarke Duncan', 'Michael Douglas', 'Michael Fassbender', 'Michael J. Fox', 'Michael Keaton', 'Michael Moore', 'Michelle Pfeiffer', 'Michelle Williams', 'Mike Myers', 'Mila Kunis', 'Montgomery Clift', 'Morgan Freeman', 'Myrna Loy', 'Naomi Watts', 'Natalie Portman', 'Natalie Wood', 'Nick Nolte', 'Nicolas Cage', 'Nicole Kidman', 'Nina Dobrev', 'Octavia Spencer', 'Olivia de Havilland', 'Omar Sharif', 'Oprah Winfrey', 'Orson Welles', 'Owen Wilson', 'Patricia Clarkson', 'Patrick Stewart', 'Patrick Swayze', 'Patty Duke', 'Paul Giamatti', 'Paul Newman', 'Penélope Cruz', 'Peter Dinklage', 'Peter Falk', 'Peter Lorre', "Peter O'Toole", 'Peter Sellers', 'Peter Ustinov', 'Philip Seymour Hoffman', 'Pierce Brosnan', 'Quentin Tarantino', 'Rachel McAdams', 'Rachel Weisz', 'Ralph Fiennes', 'Ray Liotta', 'Reese Witherspoon', 'Renée Zellweger', 'Richard Burton', 'Richard Dreyfuss', 'Richard Gere', 'Richard Harris', 'Rita Hayworth', 'Robert De Niro', 'Robert Downey Jr.', 'Robert Duvall', 'Robert Mitchum', 'Robert Pattinson', 'Robert Redford', 'Robin Williams', 'Robin Wright', 'Rosalind Russell', "Rosie O'Donnell", 'Roy Scheider', 'Russell Crowe', 'Ryan Gosling', 'Sally Field', 'Salma Hayek', 'Samuel L. Jackson', 'Sandra Bullock', 'Sarah Silverman', 'Scarlett Johansson', 'Sean Bean', 'Sean Connery', 'Sean Penn', 'Selena Gomez', 'Seth Rogan', 'Sharon Stone', 'Shelley Winters', 'Shia LaBeouf', 'Shirley MacLaine', 'Shirley Temple', 'Sidney Poitier', 'Sigourney Weaver', 'Sissy Spacek', 'Sophia Loren', 'Spencer Tracy', 'Stanley Tucci', 'Steve Buscemi', 'Steve Martin', 'Steve McQueen', 'Stockard Channing', 'Susan Hayward', 'Susan Sarandon', 'Sylvester Stallone', 'Thelma Ritter', 'Tilda Swinton', 'Tim Curry', 'Tim Robbins', 'Tim Roth', 'Tina Fey', 'Tom Cruise', 'Tom Hanks', 'Tom Hardy', 'Tom Selleck', 'Tommy Lee Jones', 'Toni Collette', 'Tony Curtis', 'Tori Spelling', 'Tyler Perry', 'Uma Thurman', 'Vanessa Redgrave', 'Vera Farmiga', 'Viggo Mortensen', 'Vin Diesel', 'Vince Vaughn', 'Vincent Price', 'Viola Davis', 'Vivien Leigh', 'Walter Matthau', 'Wanda Sykes', 'Wesley Snipes', 'Whoopi Goldberg', 'Will Ferrell', 'Will Smith', 'Willem Dafoe', 'William H. Macy', 'William Holden', 'William Hurt', 'Winona Ryder', 'Woody Allen', 'Woody Harrelson', 'Yul Brynner', 'Yvonne De Carlo', 'Zac Efron', 'Zoe Saldana', 'Zooey Deschanel']
famous_studios = ['Disney', 'Dreamworks', 'Fox', 'Lionsgate', 'MGM', 'Paramount', 'Sony', 'Universal', 'Warner', 'Weinstein']

# Prepare data
X = []
for i, (movie_title, movie_data) in enumerate(movie_data.items()):
    # Prepare rating
    x_rating = [0] * len(all_ratings)
    if 'rating' in movie_data.keys():
        movie_rating = movie_data['rating']
        for index, rating in enumerate(all_ratings):
            if rating == movie_rating:
                x_rating[index] = 1

    # Prepare genres
    x_genres = [0] * len(all_genres)
    if 'genres' in movie_data.keys():
        movie_genres = movie_data['genres']
        for index, genre in enumerate(all_genres):
            if genre in movie_genres:
                x_genres[index] = 1

    # Prepare directors
    x_directors = [0] * len(famous_directors)
    if 'directors' in movie_data.keys():
        movie_directors = movie_data['directors']
        for index, director in enumerate(famous_directors):
            if director in movie_directors:
                x_directors[index] = 1

    # Prepare runtime
    x_runtime = [100]
    if 'runtime' in movie_data.keys():
        x_runtime[0] = movie_data['runtime']

    # Prepare studios
    x_studios = [0] * len(famous_studios)
    if 'studio' in movie_data.keys():
        movie_studio = movie_data['studio']
        for index, studio in enumerate(famous_studios):
            if studio in movie_studio:
                x_studios[index] = 1

    # Prepare actors
    x_actors = [0] * len(famous_actors)
    if 'cast' in movie_data.keys():
        movie_actors = movie_data['cast']
        for index, actor in enumerate(famous_actors):
            if actor in movie_actors:
                x_actors[index] = 1

    # Glue together all features and insert into X
    x = x_rating + x_genres + x_directors + x_runtime + x_studios + x_actors
    X.append(x)

# Load model
model = pickle.load(open('model.sav', 'rb'))

# predict
print(model.predict(X))

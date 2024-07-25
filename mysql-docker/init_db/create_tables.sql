CREATE TABLE IF NOT EXISTS clienti(
clientiId int AUTO_INCREMENT PRIMARY KEY ,
nome VARCHAR (45) NOT NULL
);

CREATE TABLE IF NOT EXISTS ordine(
codordine int AUTO_INCREMENT ,
cliente int,
data date,
PRIMARY KEY(codordine),
FOREIGN KEY(cliente) REFERENCES clienti(clientiId)
);

CREATE TABLE IF NOT EXISTS prodotto(
codiceprod int AUTO_INCREMENT ,
nomeprod VARCHAR(45) NOT NULL ,
prezzoprod  int,
giacenza int,
PRIMARY KEY(codiceprod)
);

CREATE TABLE IF NOT EXISTS forniture(
idforniture int AUTO_INCREMENT,
codordine int,
codiceprod int,
ricambi int,
qt int ,
PRIMARY KEY(idforniture),
FOREIGN KEY(codordine) REFERENCES ordine(codordine),
FOREIGN KEY(codiceprod) REFERENCES prodotto(codiceprod)
);



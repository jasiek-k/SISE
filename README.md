DFS, BFS and A* algorithms implemented to solve 15 Puzzle game, using Python.
---
BFS (iteracyjnie):
1. Wczytujemy początkowy układ planszy
2. Tworzymy pustą kolejke Q i listę stanów odwiedzonych
3. W kolejce umieszczamy układ początkowy
4. Ten układ oznaczamy jako odwiedzony
5. Pętla, dopóki kolejka nie jest pusta:
	5.1 Pobieramy z kolejki układ
	5.2 Sprawdzamy czy nie stanowi on rozwiązania
    -> Jeśli tak, to kończymy działanie algorytmu
	5.3 Sprawdzamy jakie ruchy możemy wykonać (UDRL) i
	porównujemy je z kolejnością ruchów podaną jako 
	parametr wywołania
	5.4 Przekształcamy planszę wykonując określony ruch i 
	dodajemy ją do kolejki, jeśli dany układ nie został 
	wcześniej odwiedzony (powtarzamy dla wszystkich ruchów
	jakie możemy wykonać) 
6. Jeśli pętla się zakończy bez znalezienia rozwiązania 
-> zwracamy informację o braku rozwiązania

DFS (rekurencyjnie):
1. Wczytujemy początkowy układ planszy
2. Wywołujemy rekurencyjnie funkcję dfs
3. Sprawdzamy, czy został osiągnięty maksymalny dozwolony poziom
rekurencji 
-> jeśli tak, to zwracamy None i rozpoczynamy nawrót
-> jeśli nie, to kontynuujemy
4. Sprawdzamy, czy układanka jest rozwiązana
-> jeśli tak, to kończymy działanie algorytmu
5. Odpytujemy o sąsiedztwo danej planszy i dla każdego z 
możliwych ruchów:
    5.1 Poruszamy pustym polem
    5.2 Dodajemy przekształconą planszę do listy stanów odwiedzonych
    5.3 Wywołujemy funkcję dla przekształconej planszy
    5.4 Sprawdzamy czy stanowi ona rozwiązanie 
    -> jeśli tak - kończymy
    -> jeśli nie - wracamy do punktu 3 
Jeśli funkcja nie znajdzie rozwiązania, po wykonaniu odpowiedniej
liczby nawrotów to wynikiem jej działania będzie None.

A*:
1. Wczytujemy początkowy układ planszy
2. Dodanie układu do kolejki do przetworzenia
Pętla(dopóki coś jest do przetworzenia):
3. Sprawdzeine kosztów i wybranie układu o najmniejszym; zdjęcie go z kolejki
4. Sprawdzenie możliwych do wykonania ruchów
5. Dla Każdego ruchu:
	5.1 wykonanie ruchu i dopisanie go do długości rozwiązania
	5.2 sprawdzenie czy nowy układ nie był już przetworzony, jak nie to dopisanie go do prztworzonych i:
	5.3 sprawdzenie czy jest rozwiązaniem, jak tak, to zakończ, jak nie to:
	5.4 obliczenie kosztu ruchu z uwzględnieniem heurestyki
	5.4 dodanie nowego układu do kolejki do przetworzenia
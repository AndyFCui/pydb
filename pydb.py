import pymysql

'''
This program is working for the build basic action for 'librarydb' task.
Author: Andy(Xiang-Yu) Cui
Date: Mar 23, 2023
python: 3.8
package: pymysql
'''


def work():
    print("### Please Login With Your Username and Password ###")
    user_name = input("username: ")
    passwd = input("password: ")

    try:
        cnx = pymysql.connect(
            host='localhost',
            user=user_name,
            password=passwd,
            db='librarydb',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.err.OperationalError as e:
        print('Connection failed, Error: %d: %s' % (e.args[0], e.args[1]))
        print('Connection failed:{}'.format(e))
        exit()

    cur = cnx.cursor()
    return cur, cnx


def prompt_user_for_genre():
    print("### Select A Particular Book Genre ###")
    genre_input = input("genre: ")
    return genre_input


def get_genres(cur):
    stmt_select = "SELECT genre FROM book_genre"
    cur.execute(stmt_select)
    result = cur.fetchall()  # Fetch the query results
    return [row['genre'] for row in result]


def display_genres(genres):
    print("Available genres:")
    for i, genre in enumerate(genres, start=1):
        print(f"[{i}]: {genre}")


def validate_genre(user_input, genres):
    return user_input in genres


def display_books(books):
    print("Books In The Selected Genre:")
    for i, book in enumerate(books, start=1):
        print(f"[{i}]: ISBN: {book['isbn']}, "
              f"Author: {book['author']}, "
              f"Page_Count: {book['page_count']}, "
              f"Publisher: {book['publisher_name']}")


def main():
    cur = None  # cur is cursor of database(MySQL)
    cnx = None  # cnx is connection of database(MySQL)

    try:
        cur, cnx = work()
        genres = get_genres(cur)
        display_genres(genres)

        while True:
            user_input = prompt_user_for_genre()

            if validate_genre(user_input, genres):
                print("[STATUS]: valid genre entered.")
                cur.callproc('book_has_genre', (user_input,))
                result = cur.fetchall()
                display_books(result)
                break
            else:
                print("[STATUS]: Invalid genre, please enter a genre from the list.")
                print("Please Enter A Valid Genre From The List. --- (DO NOT INCLUDE IDX) ---")
    finally:
        if cur is not None:
            cur.close()
        if cnx is not None:
            cnx.close()


if __name__ == '__main__':
    main()

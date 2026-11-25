import database

def main():
    database.setup_database()

    print("\n=== Travel Ticket Booking System ===\n")

    routes = database.get_all_routes()

    print("Available Routes:")
    print("-" * 65)
    for r in routes:
        status = f"Available Seats: {r[4]}" if r[4] > 0 else "Sold Out"
        print(
            f"[{r[0]}] {r[1]} | Bus: {r[2]} | Price: {r[3]} MMK | {status}"
        )
    print("-" * 65)

    try:
        choice = int(input("\nSelect a route number: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    selected_route = database.get_route_by_id(choice)

    if not selected_route:
        print("Route not found.")
        return

    if selected_route[4] <= 0:
        print(
            f"\nSorry, {selected_route[1]} ({selected_route[2]}) is sold out."
        )
        return

    name = input("Enter passenger name: ")
    seat = input("Enter seat number (e.g., A1, B4): ").upper()

    if database.is_seat_taken(choice, seat):
        print(f"\nSorry, seat {seat} is already taken.")
        return

    database.save_booking(name, choice, seat)

    print("\n" + "=" * 42)
    print("       BOOKING CONFIRMED")
    print("=" * 42)
    print(f"Passenger : {name}")
    print(f"Route     : {selected_route[1]}")
    print(f"Bus       : {selected_route[2]}")
    print(f"Seat No.  : {seat}")
    print(f"Price     : {selected_route[3]} MMK")
    print("=" * 42)


if __name__ == "__main__":
    main()
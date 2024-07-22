document.addEventListener('DOMContentLoaded', () => {
    const seats = document.querySelectorAll('.seat:not(.taken)');
    const seatInput = document.getElementById('chosen_seat');

    seats.forEach(seat => {
        seat.addEventListener('click', () => {
            // Deselect any previously selected seat
            seats.forEach(s => {
                s.classList.remove('selected');
                s.style.backgroundColor = 'red';
            });

            // Select the clicked seat
            seat.classList.add('selected');
            seat.style.backgroundColor = 'green';
            seatInput.value = seat.getAttribute('data-seat');
        });
    });
});

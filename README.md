<b>Coding Circuit Rating System</b>

This project implements a simulation of a competitive coding rating system for a series of events called the **"Coding Circuit"**. Participants’ ratings dynamically evolve after each event based on performance, contest difficulty, and inactivity.

<hr>

<b>Files</b>

- 'Participant_details.csv' – Contains participant numbers and a list of events each participated in.
- 'event_weights.csv' – Contains each event’s number, difficulty (1=Easy, 2=Medium, 3=Hard), and weight.
- 'ccrs.py' – The main Python script that performs the simulation.

<hr>

<b>Features</b>

- 6 problems per contest; difficulty determines expected solve rate.
- Dynamic rating updates based on expected vs actual performance.
- Contest 'weight factor' scales the rating impact.
- 'Decay system' for participants who miss 2+ events in a row.
- Flexible rating adjustments in early stages (first two contests).
- Biased random generation for simulating real-world solving ability.

<hr>

<b>Rating System</b>

- Initial Rating: 1000 (minimum rating = 1000)
- Expected Problems Solved (μ): 
  
  μ(R) = 6/{1 + 10^{(R_{mid} - R)/400}}
  
  where Rmid depends on contest difficulty:
  - Easy (1): Rmid = 1400  
  - Medium (2): Rmid = 1500  
  - Hard (3): Rmid = 1600
- Actual Problems Solved (S): Generated using a biased distribution.
- Rating Update Formula:  

  Δ=K⋅(S−μ)⋅weight
   
  where K = 40 for <3 events, otherwise K = 20.

<hr>

<b>Biased Problem Solving</b>

| Rating Range   | Likely Problems Solved       |
|----------------|-------------------------------|
| <1300          | 1 or 2 (highly likely)         |
| 1300–1500      | 3 (most likely)                |
| 1500–1800      | 4 or 5 (most likely)           |
| 1800+          | 6 (most likely)                |

Random values are chosen with weighted bias to simulate realistic performance tendencies.

<hr>

<b>Inactivity & Decay</b>

If a participant misses 2+ consecutive events, their rating decays:
- Decay Formula:
- 
Rnew =R−min(50,0.05⋅(R−1000)) (capped at 50 points).

- Applied only when a 2-event gap is detected between participations.

<hr>

<b>Output Files</b>

- 'rating_history.csv'  
  Ratings of every participant after each event (even if they didn’t participate, rating is carried forward or decayed).
  
- 'final_leaderboard.csv'  
  Final ratings, sorted from highest to lowest.

<hr>

<b>How to Run</b>

1. Ensure Python 3.7+ is installed.
2. Install required package (if not already installed):
   ```
   pip install pandas
   ```
3. Place both CSV input files in the same directory as `ccrs.py`.
4. Run the script:
   ```
   python ccrs.py
   ```
5. Check the generated files: `rating_history.csv` and `final_leaderboard.csv`.

---

<b>Notes</b>

- All ratings are rounded to the nearest integer.
- Decay is applied before event participation if the inactivity condition is met.
- The simulation ensures a fair and dynamic rating evolution based on real-world contest behavior.



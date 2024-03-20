from models import db, Movie, Producer, Studio
from sqlalchemy import text
import pandas as pd
from utils.data_importer import download_file
from typing import List, TypedDict

class WorstProducersStatisticsItem(TypedDict):
    producer: str
    interval: int
    previousWin: int
    followingWin: int

class WorstProducersStatistics(TypedDict):
    max: List[WorstProducersStatisticsItem]
    min: List[WorstProducersStatisticsItem]


def import_csv_to_database(file_path_or_url: str) -> None:

    if file_path_or_url.startswith('http'):
        file_path = download_file(file_path_or_url)
    else:
        file_path = file_path_or_url

    movies_df = pd.read_csv(file_path, delimiter=';')
    movies_df['winner'] = movies_df['winner'].fillna('').apply(lambda x: x.strip().lower() == 'yes')
    
    for _, row in movies_df.iterrows():
        producer_names = row['producers'].replace(' and ', ',').split(',')
        producers = []
        for name in producer_names:
            name = name.strip()
            if not name:
                continue
            producer = Producer.query.filter_by(name=name).first()
            if not producer:
                producer = Producer(name=name)
                db.session.add(producer)
            
            producers.append(producer)
        
        studio_names = row['studios'].split(',')
        studios = []
        for name in studio_names:
            name = name.strip()
            studio = Studio.query.filter_by(name=name).first()
            if not studio:
                studio = Studio(name=name)
                db.session.add(studio)
            studios.append(studio)

        movie = Movie.query.filter_by(title=row['title'], year=row['year']).first()
        if movie:
            movie.winner=row['winner']
            movie.producers = producers
            movie.studios = studios

            db.session.add(movie)
        else:
            movie = Movie(
                title=row['title'],
                year=row['year'],
                winner=row['winner'],
                producers=producers,
                studios=studios
            )
            db.session.add(movie)
    
    db.session.commit()

def get_producers_intervals() -> WorstProducersStatistics:
    sql_query = text("""
        WITH WinnerYears AS (
            SELECT
                p.name AS producer_name,
                m.year,
                LAG(m.year) OVER (PARTITION BY p.name ORDER BY m.year) AS previous_year
            FROM
                movie m
            JOIN
                movie_producer mp ON m.id = mp.movie_id
            JOIN
                producer p ON mp.producer_id = p.id
            WHERE
                m.winner = TRUE
        ),
        Intervals AS (
            SELECT
                producer_name,
                year - previous_year AS interval,
                previous_year,
                year AS following_year
            FROM
                WinnerYears
            WHERE
                previous_year IS NOT NULL
        ),
        MinIntervals AS (
            SELECT
                producer_name,
                interval,
                previous_year,
                following_year
            FROM
                Intervals
            WHERE
                interval = (SELECT MIN(interval) FROM Intervals)
        ),
        MaxIntervals AS (
            SELECT
                producer_name,
                interval,
                previous_year,
                following_year
            FROM
                Intervals
            WHERE
                interval = (SELECT MAX(interval) FROM Intervals)
        ),
        Results AS (
            SELECT
                'min' AS type,
                producer_name,
                interval,
                previous_year,
                following_year
            FROM
                MinIntervals
            UNION ALL
            SELECT
                'max' AS type,
                producer_name,
                interval,
                previous_year,
                following_year
            FROM
                MaxIntervals
        )
                     
        SELECT * FROM Results ORDER BY following_year ASC
        
    """)
    
    result = db.engine.execute(sql_query)
    response = {
        "min": [],
        "max": []
    }
    for row in result:
        item = {
            'producer': row.producer_name, 
            'interval': row.interval,
            'previousWin': row.previous_year,
            'followingWin': row.following_year,
        }
        if row.type == 'max':
            response["max"].append(item)
        else:
            response["min"].append(item)
    
    return response

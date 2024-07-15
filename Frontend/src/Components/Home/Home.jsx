import React, { useEffect, useState } from "react";
import Alert from '@mui/material/Alert';
import Stack from '@mui/material/Stack';

import "./Home.scss";
import axios from "axios";
import { Link } from "react-router-dom";
import { BiPlay } from "react-icons/bi";
import { AiOutlinePlus } from "react-icons/ai";

const apiKey = "7e5122f42b3d47b2f9c1deaf4e1d2214";
const url = "https://api.themoviedb.org/3";
const imgUrl = "https://image.tmdb.org/t/p/original";
const upcoming = "upcoming";
const nowPlaying = "now_playing";
const popular = "popular";
const topRated = "top_rated";
const recommended = "recommendations"; // Add a new constant for recommended movies

const Card = ({ img }) => <img className="card" src={img} alt="cover" />;

const Row = ({ title, arr = [] }) => (
  <div className="row">
    <h2>{title}</h2>

    <div>
      {arr.map((item, index) => (
        <Card key={index} img={`${imgUrl}/${item.poster_path}`} />
      ))}
    </div>
  </div>
);


const Home = () => {
  const [upcomingMovies, setUpcomingMovies] = useState([]);
  const [nowPlayingMovies, setNowPlayingMovies] = useState([]);
  const [popularMovies, setPopularMovies] = useState([]);
  const [topRatedMovies, setTopRatedMovies] = useState([]);
  const [recommendedMovies, setRecommendedMovies] = useState([]); // Add state for recommended movies
  const [genre, setGenre] = useState([]);
  // Define a state variable to track liked movies
  const [likedMovies, setLikedMovies] = useState([]);

  useEffect(() => {
    const fetchUpcoming = async () => {
      const {
        data: { results },
      } = await axios.get(`${url}/movie/${upcoming}?api_key=${apiKey}`);
      setUpcomingMovies(results);
    };
    const fetchNowPlaying = async () => {
      const {
        data: { results },
      } = await axios.get(`${url}/movie/${nowPlaying}?api_key=${apiKey}`);
      setNowPlayingMovies(results);
    };
    const fetchPopular = async () => {
      const {
        data: { results },
      } = await axios.get(`${url}/movie/${popular}?api_key=${apiKey}`);
      setPopularMovies(results);
    };
    const fetchTopRated = async () => {
      const {
        data: { results },
      } = await axios.get(`${url}/movie/${topRated}?api_key=${apiKey}`);
      setTopRatedMovies(results);
    };

    const getAllGenre = async () => {
      const {
        data: { genres },
      } = await axios.get(`${url}/genre/movie/list?api_key=${apiKey}`);
      setGenre(genres);
      console.log(genres);
    };

    getAllGenre();

    fetchUpcoming();
    fetchNowPlaying();
    fetchPopular();
    fetchTopRated();

    async function fetchRecommended() {
      try {
        // Check local storage for liked movies
        const storedLikedMovies = JSON.parse(localStorage.getItem('likedMovies'));
    
        // Check local storage for familyFriendly
        const familyFriendly = JSON.parse(localStorage.getItem('familyFriendly'));
    
        // Define the request data with default values
        const requestData = {
          movie1: 317442,
          movie2: 244478,
          languages: JSON.parse(localStorage.getItem('lang')),
          adult: familyFriendly ? 1 : 0, // Set "adult" based on the familyFriendly value
        };
    
        // Use liked movies from local storage if available
        if (storedLikedMovies && storedLikedMovies.length >= 2) {
          requestData.movie1 = storedLikedMovies[0];
          requestData.movie2 = storedLikedMovies[1];
        }
    
        // Make a POST request to the recommended movies endpoint
        const response = await axios.post("http://localhost:8000/recommendMovies", requestData);
        console.log(response.data);
        // Update the state with recommended movies data
        setRecommendedMovies(response.data.recommendations);
      } catch (error) {
        console.error("Error fetching recommended movies:", error);
      }
    }
    
    

    // Call the fetchRecommended function when the component is mounted
    fetchRecommended();

  }, []);

  // Define a function to handle liking a movie
  const handleLikeMovie = (movieId) => {
    alert("Added to Liked Movies");
    // Check if the movie is already liked
    if (!likedMovies.includes(movieId)) {
      // Add the movie ID to the liked movies list
      const updatedLikedMovies = [...likedMovies, movieId];
      setLikedMovies(updatedLikedMovies);

      // Save the liked movies list in local storage
      localStorage.setItem('likedMovies', JSON.stringify(updatedLikedMovies));
    }
  };

  
  return (
    <section className="home">
      <div
        className="banner"
        style={{
          backgroundImage: popularMovies[0]
            ? `url(${`${imgUrl}/${popularMovies[0].poster_path}`})`
            : "rgb(16, 16, 16)",
        }}
      >
        {popularMovies[0] && <h1>{popularMovies[0].original_title}</h1>}
        {popularMovies[0] && <p>{popularMovies[0].overview}</p>}

        <div>
          <button>
            <BiPlay /> Play
          </button>
          <button>
            My List <AiOutlinePlus />
          </button>
        </div>
      </div>
      <div className="row">
        <h2>Recommended Movies</h2>
        <div className="card-container">
          {recommendedMovies.map((movie, index) => (
            <div key={index} className="card-container">
              <img
                className={`card ${likedMovies.includes(movie.id) ? 'liked' : ''}`}
                src={movie.poster_url}
                alt="cover"
                onClick={() => handleLikeMovie(movie.id)} // Handle click and add to liked
              />
              {likedMovies.includes(movie.id) && <div className="liked-label">Liked</div>}
            </div>
          ))}
        </div>
      </div>
      <Row title={"Upcoming"} arr={upcomingMovies} />
      {/* <Row title={"Now Playing"} arr={nowPlayingMovies} /> */}
      {/* <Row title={"Popular"} arr={popularMovies} /> */}
      {/* <Row title={"Top Rated"} arr={topRatedMovies} /> */}



    </section>
  );
};

export default Home;

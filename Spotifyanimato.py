import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Spotify credentials (replace these with your actual username and password)
SPOTIFY_USERNAME = "your_spotify_username"
SPOTIFY_PASSWORD = "your_spotify_password"

# Function to initialize and return the driver with options
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")  # Open in Incognito mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU (useful for headless)
    chrome_options.add_argument("--headless")  # Uncomment to run in headless mode
    chrome_options.add_argument("--window-size=1920x1080")  # Set window size for headless mode

    # Set up WebDriver
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    return driver

# Function to log into Spotify
def login_to_spotify(driver):
    try:
        driver.get("https://open.spotify.com/")
        
        # Wait for the login button and click it
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="Log in"]'))
        ).click()
        
        # Wait for the username input field to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "login-username"))
        ).send_keys(SPOTIFY_USERNAME)

        # Wait for the password input field to load and type the password
        password_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "login-password"))
        )
        password_field.send_keys(SPOTIFY_PASSWORD)
        
        # Click the login button
        driver.find_element(By.XPATH, '//button[@data-testid="login-button"]').click()

        # Wait for the login to complete (home page or dashboard visible)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="Root__root-sc-1sm5v6t-0 gmIuPg"]'))
        )
        time.sleep(5)  # Allow time for the page to fully load

    except Exception as e:
        print(f"Login failed: {e}")
        driver.quit()
        exit()

# Function to create or play the playlist
def create_or_play_playlist(driver):
    try:
        # Search for the artists "Rxyykon" and "yxngrebel"
        search_query = "Rxyykon yxngrebel"
        driver.get(f"https://open.spotify.com/search/{search_query}")

        # Wait for search results to load and check if any songs are found
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-testid="search-results"]'))
        )
        
        # Check if the playlist already exists
        playlist_name = "streams"
        driver.get(f"https://open.spotify.com/playlist/{playlist_name}")

        try:
            # If the playlist exists, play it on repeat
            play_button = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Play"]'))
            )
            play_button.click()
            print(f"Playing the playlist '{playlist_name}' on repeat.")
        
        except Exception as e:
            print(f"Playlist '{playlist_name}' does not exist, creating a new one: {e}")
            # Create the playlist if it doesn't exist
            driver.get(f"https://open.spotify.com/playlist/{playlist_name}")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Create Playlist"]'))
            ).click()

            print(f"Created a new playlist '{playlist_name}'. Adding songs...")
            
            # Here you can add songs manually or use the API to populate the playlist

            print(f"Playlist '{playlist_name}' created successfully!")
    
    except Exception as e:
        print(f"Error in creating or playing the playlist: {e}")
        driver.quit()

# Main execution function
def main():
    driver = get_driver()

    try:
        login_to_spotify(driver)
        create_or_play_playlist(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

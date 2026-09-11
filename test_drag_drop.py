import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    """Fixture to initialize and close the WebDriver browser instance."""
    options = webdriver.ChromeOptions()
    # Optional: Run in headless mode for CI/CD environments
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_positive_drag_and_drop(driver):
    """
    Positive Test Case: Successfully drag the white rectangular box
    and drop it into the yellow rectangular box.
    """
    # Step 1: Navigate to the target URL
    url = "https://jqueryui.com"
    driver.get(url)

    # Step 2: Handle the iframe containing the draggable elements
    # The elements live inside a demo iframe, so we must switch to it first.
    wait = WebDriverWait(driver, 10)
    demo_frame = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "demo-frame")))
    driver.switch_to.frame(demo_frame)

    # Step 3: Locate source (draggable) and target (droppable) elements
    source_element = wait.until(EC.visibility_of_element_located((By.ID, "draggable")))
    target_element = driver.find_element(By.ID, "droppable")

    # Step 4: Perform the Drag and Drop operation using ActionChains
    actions = ActionChains(driver)
    actions.drag_and_drop(source_element, target_element).perform()

    # Step 5: Verification (Assertion)
    # Upon a successful drop, the target element text changes to "Dropped!"
    success_text = target_element.text
    assert success_text == "Dropped!", f"Expected 'Dropped!', but got '{success_text}'"


def test_negative_drag_and_drop_miss(driver):
    """
    Negative Test Case: Move the draggable element to an offset position
    outside the target box, ensuring it does not trigger a successful drop.
    """
    url = "https://jqueryui.com"
    driver.get(url)

    # Switch to the demo iframe
    wait = WebDriverWait(driver, 10)
    demo_frame = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "demo-frame")))
    driver.switch_to.frame(demo_frame)

    source_element = wait.until(EC.visibility_of_element_located((By.ID, "draggable")))
    target_element = driver.find_element(By.ID, "droppable")

    # Move by offset away from the target instead of dragging onto it
    actions = ActionChains(driver)
    actions.drag_and_drop_by_offset(source_element, 300, 300).perform()

    # Verification (Assertion)
    # The text should still remain "Drop here" and not change to "Dropped!"
    failed_text = target_element.text
    assert failed_text == "Drop here", f"Box registered a drop unexpectedly. Text: '{failed_text}'"

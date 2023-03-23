try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
except Exception as exception:
    exception.with_traceback()



class browser():
    def __init__(self, headless=True, useDetailedAnswer=False, useCreativeAnswer=True, Debug=False, DebugQuery='', DebugTimeout=30, DebugIterations=10, DebugVerbose=False):
        options = uc.ChromeOptions()
        if headless:
            options.add_argument('--headless') 
        self.driver = uc.Chrome(options=options)
        try:
            self.driver.get('https://staging.phind.com/')
            self.driver.execute_script("localStorage.setItem('useDetailedAnswer', "+str(useDetailedAnswer).lower()+")")
            self.driver.execute_script("localStorage.setItem('useCreativeAnswer', "+str(useCreativeAnswer).lower()+")")
        except Exception as exception:
            exception.with_traceback()
        if Debug:
            self._search_average_test(query=DebugQuery, timeout=DebugTimeout, iterations=DebugIterations, verbose=DebugVerbose)
            
    
    def search(self, query='',timeout=30):
        self.driver.get('https://staging.phind.com/search?q='+query)
        self.wait = WebDriverWait(self.driver, timeout)
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div/div/span')))
            search_results = self.driver.find_element('xpath', '/html/body/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div/div/span').text
            return search_results
        except:
            print('Search Timeout error. Time exceeded ', timeout, ' seconds.')
    def search_stream(self, query='', timeout=10, max_elements=20,retries_max=10):
        self.driver.get('https://staging.phind.com/search?q='+query)
        self.wait = WebDriverWait(self.driver, timeout)
        retries=0
        for i in range(max_elements):
            print('Searching for element ', i)
            while retries<retries_max:
                try:
                    self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div/div/span/*['+str(i)+']')))
                    element = self.driver.find_element('xpath', '/html/body/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div/div/span/*['+str(i)+']').text
                    print(element)
                    if element!='':
                        retries=0
                    break
                except:
                    print('Element not found. Retrying in ', timeout, ' seconds.')
                    retries+=1
        if retries>=retries_max:
            print('Search Timeout error. Time exceeded ', timeout, ' seconds.')
    def _search_average_test(self, query='', timeout=30, iterations=10, verbose=False):
        average_time=0
        exec_time=[]
        
        for i in range(iterations):
            timer=time.time()
            output=self.search(query=query, timeout=timeout)
            timer=time.time()-timer
            timer=timer.__round__(2)
            exec_time.append(timer)
            average_time+=timer
            if verbose:
                print('\nSearch output: ', output)
                print('Time taken to fetch: ', timer)
                
        average_time=(average_time/iterations).__round__(2)
        if verbose:
            print('\n\nAverage time taken to fetch: ', average_time, ' seconds over ', iterations, ' iterations.')
            
        return average_time
            

    def close(self):
        self.driver.quit()
    
if __name__ == '__main__':
    
    query=input('You are running a python module as a script. Please enter a query to test average time to fetch:  ')
    browser = browser(Debug=True, DebugQuery=query, DebugVerbose=True)
    browser.close()
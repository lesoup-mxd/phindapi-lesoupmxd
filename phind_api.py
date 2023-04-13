#Welcome to the Phind API. This is a python module that allows you to use the Phind search engine in your python scripts.

#depends on undetected_chromedriver, selenium, time

try:

    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
except Exception as exception:
    exception.with_traceback()
    exit()


# Define the browser class
class browser():
    def __init__(self,
        headless=True, #whether to run the browser in GUI-less mode or not
        useDetailedAnswer='Boolean', #useDetailedAnswer is deprecated, useConciseAnswer is the new option
        
        #Web search binding     #GPT4                #Shorten the answer
        useCreativeAnswer=True, useExpertMode=False, useConciseAnswer=True,
        
        #Debug options
            Debug=False, DebugQuery='', DebugTimeout=30, DebugIterations=10, DebugVerbose=False
        ):
        options = uc.ChromeOptions()
        
        #Backward compatibility
        if useDetailedAnswer==True:
            useConciseAnswer=False
        elif useDetailedAnswer==False:
            useConciseAnswer=True
            
        if headless:
            options.add_argument('--headless') 
        self.driver = uc.Chrome(options=options)
        
        #Initilaisation, Configuration of LocalStorage
        try:
            self.driver.get('https://staging.phind.com/')
            #removed useDetailedAnswer as it is deprecated, using useConciseAnswer instead
            self.driver.execute_script("localStorage.setItem('useDetailedAnswer', "+str(useConciseAnswer).lower()+")")
            self.driver.execute_script("localStorage.setItem('useCreativeAnswer', "+str(useCreativeAnswer).lower()+")")
            self.driver.execute_script("localStorage.setItem('useExpertMode', "+str(useExpertMode).lower()+")")
        except Exception as exception:
            exception.with_traceback()
        if Debug:
            out = self._search_average_test(query=DebugQuery, timeout=DebugTimeout, iterations=DebugIterations, verbose=DebugVerbose)
            
    # Define the search function, which takes a query, timeout as arguments
    def search(self, query='',timeout=30,verbose=False):
        self.driver.get('https://staging.phind.com/search?q='+query)
        self.wait = WebDriverWait(self.driver, timeout)
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.col-lg-10 > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)')))
            search_results=''
            while search_results=='':
                search_results = self.driver.find_element(By.CSS_SELECTOR, '.col-lg-10 > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)').text
                time.sleep(timeout/10)
            if verbose:
                print('Parsing data stream...')
            search_results_old = ''
            while search_results!=search_results_old or search_results=='':
                search_results_old = search_results
                search_results = self.driver.find_element(By.CSS_SELECTOR, '.col-lg-10 > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)').text
                time.sleep(timeout/15)
            return search_results
        except:
            print('Search Timeout error. Time exceeded timeout')
    
    #search_stream function will not be implemented

    #Debug function to test average time to fetch
    def _search_average_test(self, query='', timeout=30, iterations=10, verbose=False):
        average_time=0
        exec_time=[]
        
        for i in range(iterations):
            timer=time.time()
            output=self.search(query=query, timeout=timeout, verbose=verbose)
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
            
    #Terminate the browser
    def close(self,verbose=False):
        if verbose:
            print('Shutting down the spider...')
        self.driver.quit()


#If this module is ran as a script
if __name__ == '__main__':
    try:
        query=input('You are running a python module as a script. Please enter a query to fetch: ')
    except:
        exit()
    print('Initialising the spider...')
    browser = browser()
    while True:
        print('Connecting...')
        print(browser.search(query=query, verbose=True))
        query=input('Press enter to exit or enter a new query to fetch: ')
        if query=='':
            browser.close(verbose=True)
            exit()
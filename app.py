## importing libraries

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.colored_header import colored_header
import streamlit.components.v1 as component
from streamlit_lottie import st_lottie
from bs4 import BeautifulSoup, Comment
import lxml
import lxml_html_clean
import urllib.request
import requests
import pandas as pd
import numpy as np
from cleantext import clean
from pywebcopy import save_website
import zipfile
from datetime import datetime
import shutil
import json
import base64
import os
import re


######## app fumctions


### insert external css
@st.cache_data
def insert_css(css_file:str):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

### insert external html file
# @st.cache_data
def insert_html(html_file):
    with open(html_file) as f:
        return f.read()

### insert lottie animation json files
@st.cache_data
def insert_lottie_animation(animation_file:str):
    with open(animation_file, "r") as f:
        return json.load(f)



### download the text as docs
def download_text(text, filename):
    """
    download article text 
    in document format
    """
    #### Convert string to bytes
    b64 = base64.b64encode(text.encode()).decode()

    href = f"""
            <a href="data:application/octet-stream;base64,{b64}" download="{filename}">
                <button class="neon-button">Download</button>
            </a>
            """
    
    st.markdown(href, unsafe_allow_html=True)
    if __name__=="__main__":
        insert_css("cssfiles/download-btn.css")


### copy text icon
def copy_text(text):
    """
    copy text icon
    """
    html_code = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
             <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css" integrity="sha512-Kc323vGBEqzTmouAECnVceyQqyqdsSiqLQISBL29aUW4U/M7pSPA/gEUZQqv1cwx4OnYxTxve5UMg5GT6L4JJg==" crossorigin="anonymous" referrerpolicy="no-referrer" />
            <style>
                *{{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                .copy-button{{
                    font-size: 24px;
                    cursor: pointer;
                    color: #5b70f3;
                    transition: 0.3s ease-in-out;
                }}
            </style>
        </head>
        <body>
            <a class="copy-button" onclick="copyText()">
                <i class="fa-solid fa-copy"></i>
            </a>
            <br>
            <br>
            <p id="textToCopy">{text}</p>

            <script>
                function copyText() {{
                    // Get the text from the <p> tag
                    const text = document.getElementById('textToCopy').innerText;

                    // Create a temporary <textarea> element
                    const textarea = document.createElement('textarea');
                    textarea.value = text;
                    document.body.appendChild(textarea);

                    // Select the text in the <textarea>
                    textarea.select();

                    // Execute the copy command
                    document.execCommand('copy');

                    // Remove the <textarea> element from the DOM
                    document.body.removeChild(textarea);

                    alert('Text copied');
                }}
            </script>
        </body>
        </html>

    """

    component.html(html_code,height=28)




### copy and download button
def Copy_download_button(text,text_format,text_file_name):
    try:
                ### column for copy and download article
        Copy_btn_col,download_btn_col, blank_col_copy1, blank_col_copy2= st.columns([1,3,5,5],gap="small")

        with blank_col_copy1:
            st.text("")
        with blank_col_copy1:
            st.text("")
                
        with Copy_btn_col:
            copy_text(text)

        with download_btn_col:
            download_text(text=text_format,filename=text_file_name)
    except Exception as e:
        st.warning("Something went wrong...",e,icon="⚠️")


### download image
def download_image(url, filename):
    """
    it download images
    """
    try:
       
        with urllib.request.urlopen(url) as response:
            image_data = response.read()
        
        #### Encode the image in base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        #### Display  image
        st.image(url,use_column_width=True)

        href = f"""
            <a href="data:file/png;base64,{image_base64}" 
                download="{filename}">
                <button class="image-download-btn">
                    download
                </button>
            </a>
                
                """
        st.markdown(href, unsafe_allow_html=True)

        if __name__=="__main__":
            insert_css("cssfiles/image-download.css")

    except Exception as e:
        st.error(f"Failed to download image: {e}")


#######################################################

### lottie animations
@st.cache_data
def Error_lottie_animation():
    Error_404_col, page_not_found_col = st.columns(2)

    with Error_404_col:

        try:
            Error_404 = insert_lottie_animation("lottie_animations/error-404.json")
            st_lottie(
                animation_source=Error_404,
                speed=1,
                reverse=False,loop=True,
                quality="high",
                height=315,
                width=400,
                key="404 error"
            )
        except Exception as err:
            st.warning("something went wrong...",err,icon="⚠️")

    with page_not_found_col:    
                    
        try:
            page_not_found = insert_lottie_animation("lottie_animations/page-not-found.json")
            st_lottie(
                animation_source=page_not_found,
                speed=1,
                reverse=False,loop=True,
                quality="high",
                height=265,
                width=400,
                key="page not found"
            )
        except Exception as err:
            st.warning("something went wrong...",err,icon="⚠️")


#####################    main app function

#### checking url is correct or not
def check_url(url):
    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code < 511:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False


### text cleaning 
def Text_Cleaning(text)->str:
    """
    this function gives clean 
    text of the paragraphs , etc
    which makes easy to understand of the text
    """
    pattern = r'[`^]'
    cleaned_paragraph = re.sub(pattern, '', text)

    clean_text = clean(
        text=cleaned_paragraph,fix_unicode=True,
        to_ascii=True,
        no_line_breaks=False,
        keep_two_line_breaks=True
    )

    pattern = r'\[\d+\]'
    cleaned_text_output = re.sub(pattern, '', clean_text)
    return cleaned_text_output

class WebScraper:

    def __init__(self,web_url) -> any:
        """
        check url , extract web content
        and make beautifulsoup object
        """
        try:
            self.web_url = web_url
            if check_url(web_url):
                self.http_responce = requests.get(url=web_url) 
                    
                if self.http_responce.status_code == 200:   ### cheacking http responce
                    self.soup = BeautifulSoup(self.http_responce.content,"lxml")
                    
                else:
                    st.info("unable to scrap")
                    st.text("")
                    Error_lottie_animation()
            else:
                st.warning("Enter Correct url...",icon="⚠️")
                st.text("")
                Error_lottie_animation()
        except Exception as er:
            st.warning("Something went wrong...\n\n",er,icon="⚠️")

    
    #### scraping all pragraph
    def Scrap_All_Paragraph(self)->str:
        """
        scraping all paragraph p - tag
        from website
        """
        try:
            self.all_para = []   ### all paragraph list

            for i in self.soup.find_all("p"):
                self.all_para.append(Text_Cleaning(i.text))

            if len(self.all_para) > 0:
                st.markdown("<h4 style='color: #e8630a;'>Paragraph</h4>",unsafe_allow_html=True)

                st.markdown(
                    f"""
                    <span>
                        Scraped Paragraphs: <span style="color: #42b883;" >{len(self.all_para)}</span>
                    </span>
                    """,
                    unsafe_allow_html=True
                )
                st.text("")
                st.text("")
                for j in np.array(self.all_para):
                    st.write(j)

                st.text("")
                self.copy_para = " || ".join(map(str, self.all_para))
                self.download_para = "\n\n".join(map(str, self.all_para))
                st.text("")

                ### copy and downloading paragraph
                if __name__=="__main__":
                    Copy_download_button(
                        text=self.copy_para,
                        text_format=self.download_para,
                        text_file_name="paragraph.doc"
                    )

                st.text("")
                st.write("---")
        except Exception as er:
            return er
        
    
    #### scrap headings
    def Scrap_All_Heading(self)->str:
        """
        scraping all headings h1 - h6
        from website
        """

        try:
            ### all headings list h1 - h6

            self.h1_heading = []
            self.h2_heading = []
            self.h3_heading = []
            self.h4_heading = []
            self.h5_heading = []
            self.h6_heading = []

            ### scraping all headings
            for i in self.soup.find_all("h1"):
                self.h1_heading.append(i.text)

            for i in self.soup.find_all("h2"):
                self.h2_heading.append(i.text)

            for i in self.soup.find_all("h3"):
                self.h3_heading.append(i.text)

            for i in self.soup.find_all("h4"):
                self.h4_heading.append(i.text)

            for i in self.soup.find_all("h5"):
                self.h5_heading.append(i.text)

            for i in self.soup.find_all("h6"):
                self.h6_heading.append(i.text)

            st.markdown("<h4 style='color: #e8630a;'>Headings</h4>",unsafe_allow_html=True)  

            self.all_Headings_sum = len(self.h1_heading) + len(self.h2_heading) +  len(self.h3_heading) + len(self.h4_heading) + len(self.h5_heading) + len(self.h6_heading)

            st.markdown(
                f"""
                <span>
                    Scraped Headings: <span style="color: #42b883;" >{str(self.all_Headings_sum)}</span>
                </span>
                """,
                unsafe_allow_html=True
            )
            st.text("") 
            
            Heading_col1, Heading_col2, Heading_col3 = st.columns(3,gap="small")

            with Heading_col1:

                if len(self.h1_heading) > 0:
                    st.markdown("<h5>H1 - Heading</h5>",unsafe_allow_html=True)
                    st.text("")
                    for j in self.h1_heading:
                        st.write(j)
                    
                    st.text("")
                    self.copy_h1 = " || ".join(map(str, self.h1_heading))
                    st.text("")
                    copy_text(self.copy_h1)  ### coping text

                if len(self.h2_heading) > 0:
                    st.markdown("<h5>H2 - Heading</h5>",unsafe_allow_html=True)
                    st.text("")
                    for j in self.h2_heading:
                        st.write(j)
                    
                    st.text("")
                    self.copy_h2 = " || " .join(map(str, self.h2_heading))
                    st.text("")
                    copy_text(self.copy_h2)  ### coping text


            with Heading_col2:

                if len(self.h3_heading) > 0:
                    st.markdown("<h5>H3 - Heading</h5>",unsafe_allow_html=True)
                    st.text("")
                    for j in self.h3_heading:
                        st.write(j)
                    
                    st.text("")
                    self.copy_h3 = " || ".join(map(str, self.h3_heading))
                    st.text("")
                    copy_text(self.copy_h3) #### coping text
            

                if len(self.h6_heading) > 0:
                    st.markdown("<h5>H6 - Heading</h5>",unsafe_allow_html=True)
                    st.text("")
                    for j in self.h6_heading:
                        st.write(j)
                    
                    st.text("")
                    self.copy_h6 = " || ".join(map(str, self.h6_heading))
                    st.text("")
                    copy_text(self.copy_h6)  ### coping text
            

            with Heading_col3:

                if len(self.h4_heading) > 0:
                    st.markdown("<h5>H4 - Heading</h5>",unsafe_allow_html=True)
                    st.text("")
                    for j in self.h4_heading:
                        st.write(j)
                    
                    st.text("")
                    self.copy_h4 = " || ".join(map(str, self.h4_heading))
                    st.text("")
                    copy_text(self.copy_h4)

                if len(self.h5_heading) > 0:
                    st.markdown("<h5>H5 - Heading</h5>",unsafe_allow_html=True)
                    st.text("")
                    for j in self.h5_heading:
                        st.write(j)
                    
                    st.text("")
                    self.copy_h5 = " || ".join(map(str, self.h5_heading))
                    st.text("")
                    copy_text(self.copy_h5)  ##3 coping text


            st.text("")        
            st.text("")        
            st.write("---")

        except Exception as er:
            return er
        
    ### scraping website tables
    def Scrap_All_tables(self,table_url)->any:
        """
        using pandas to scrap
        website tables
        """
        try:
            self.table_url = table_url
            self.Html_table = pd.read_html(table_url) ### extract html tables
            st.markdown("<h4 style='color: #e8630a;'>Tables</h4>",unsafe_allow_html=True)

            st.markdown(
                    f"""
                    <span>
                        Scraped Tables: <span style="color: #42b883;" >{len(self.Html_table)}</span>
                    </span>
                    """,
                    unsafe_allow_html=True
                )
            st.text("")
            for i in self.Html_table:
                st.dataframe(i,use_container_width=True)
                st.text("")
                st.text("")
            st.text("")
            st.write("---")
        except Exception as err:
            st.warning("Unable to scrap Table...\n\n",err,icon="⚠️")

    
    ### scraping all ordered and unordered list
    def Scrap_All_list(self)->str:
        """
        it scrap ul and ol tags list
        """

        try:
            self.Html_list = []
            
            for i in self.soup.find_all("li"):
                self.Html_list.append(Text_Cleaning(i.text))

            if len(self.Html_list) > 0:
                st.markdown("<h4 style='color: #e8630a;'>List</h4>",unsafe_allow_html=True)

                st.markdown(
                    f"""
                    <span>
                        Scraped List: <span style="color: #42b883;" >{len(self.Html_list)}</span>
                    </span>
                    """,
                    unsafe_allow_html=True
                )
                st.text("")
                for j in np.array(self.Html_list):
                    st.write(j)
                st.text("")
                self.copy_list = " || ".join(map(str, self.Html_list))
                self.download_list = "\n\n".join(map(str, self.Html_list))
                st.text("")
                
                ### download and copy button
                if __name__=="__main__":
                    Copy_download_button(
                        text=Text_Cleaning(self.copy_list),
                        text_format=Text_Cleaning(self.download_list),
                        text_file_name="Website list.doc"
                    )

                st.text("")
                st.text("")
                st.write("---")

        except Exception as e:
            return e
        
    
    ### scraping all links 
    def Scrap_All_links(self)->any:
        """
        scraping all links text
        tag name <a> - anchor tag
        """

        try:

            self.link_name = []
            self.link_url = []
            self.links = []  ### list of http links

            if self.http_responce.status_code == 200:
                st.markdown(
                    """
                    <h4 style="color: orangered;">
                        Links
                    </h4>
                    """
                    ,unsafe_allow_html=True)
                
                st.text("")
                for a_tag in self.soup.find_all('a', href=True):
                    self.href = a_tag['href']
                    if self.href.startswith('https://'):
                        self.anchor_text = Text_Cleaning(a_tag.get_text(strip=True)) ### Get anchor text
                        self.links.append(self.href)
                        st.write(f"{self.anchor_text} - {self.href}") 

                        self.link_name.append(self.anchor_text)
                        self.link_url.append(self.href)

                st.markdown(
                    f"""
                    <span>
                        Scraped Links: <span style="color: #42b883;" >{len(self.links)}</span>
                    </span>
                    """,
                    unsafe_allow_html=True
                )

                self.Name_link = [f"{i} - {j}" for i,j in zip(self.link_name,self.link_url)]

                self.download_link = "\n\n".join(map(str, self.Name_link))
                st.text('')
                st.text('')
                if __name__=="__main__":
                    download_text(
                        text=self.download_link,
                        filename="link.doc"
                    )
                st.text("")
                st.text("")
                st.write("---")

        except Exception as e:
            return  e
        
    ### all text of website
    def Scrap_All_text(self)->any:
        """
        it scrap text which is not
        present in p tag
        """

        try:
            st.text("")
            self.all_text  = self.soup.get_text()  ### scraping clean text
            self.all_text_value = Text_Cleaning(self.all_text)

            st.markdown(
                """
                <h4 style="color: orangered;">
                    All text
                </h4>
                """
                ,unsafe_allow_html=True)
            st.text("")

            st.write(self.all_text_value)

            
            self.download_all_text = Text_Cleaning(self.all_text)

            if __name__=="__main__":
                download_text(
                    text=self.download_all_text,
                    filename="all-text.doc"
                )

            st.text("")
            st.write("---")
        except Exception as e:
            return e



    ### scraping span tag text
    def Scrap_Span_text(self)->any:
        """
        it scraps the text present
        inside span tag
        """    
        
        try:
            self.span_text = []  ###  span tag list
            for i in self.soup.find_all("span"):
                self.span_text.append(i.text)
            
            if len(self.span_text) > 0:
                st.text("")
                st.text("")
                st.markdown(
                    """
                    <h4 style="color: orangered;">
                        span tag text
                    </h4>
                    """,unsafe_allow_html=True)
                
                st.markdown(
                    f"""
                    <span>
                        Scraped Span Text: <span style="color: #42b883;" >{len(self.span_text)}</span>
                    </span>
                    """,
                    unsafe_allow_html=True
                )
                
                st.text("")
                for j in set(self.span_text):
                    st.write(Text_Cleaning(j))    

                
                st.text("")
                st.text("")

                self.download_span_text = "\n\n".join(map(str, set(self.span_text)))

                if __name__=="__main__":
                    download_text(  ### downloading text
                        text=Text_Cleaning(self.download_span_text),
                        filename="span-text.doc"
                    )

                st.text("")
                st.write("---")
        except Exception as err:
            return err
        

    ### scraping div tag text
    def Scrap_Div_text(self)->any:
        """
        it scrap all test
        present inside div tag
        """
        try:
                        
            self.div_text = []

            for i in self.soup.find_all("div"):
                self.div_text.append(i.text)

            st.text("")
            st.markdown(
                """
                <h4 style="color: orangered;">
                    div tag text
                </h4>
                """,unsafe_allow_html=True)
            
            st.markdown(
                    f"""
                    <span>
                        Scraped Div Text: <span style="color: #42b883;" >{len(self.div_text)}</span>
                    </span>
                    """,
                    unsafe_allow_html=True
                )
            st.text("")

            for j in set(self.div_text):
                st.write(Text_Cleaning(j))

            
            self.download_div_text = "\n\n".join(map(str, set(self.div_text)))
                
            if __name__=="__main__":
                download_text(  ### downloading text
                    text=Text_Cleaning(self.download_div_text),
                    filename="span-text.doc"
                )
                
            st.text("")
            st.text("")
            st.write("---")
        except Exception as e:
            return e
        

    ### scraping html comments
    def Scrap_Comments(self)->any:
        """
        it scrap comments present
        in html code
        """    

        try:
           
            ### comments list
            self.comments = re.findall(r'<!--(.*?)-->', self.http_responce.text, re.DOTALL)
            
            
            if len(self.comments) > 0:
                st.markdown(
                    """
                        <h4 style="color: orangered;">
                            comments 
                        </h4>
                        """,unsafe_allow_html=True)
                
                st.markdown(
                    f"""
                    <span>
                        Scraped Comments: <span style="color: #42b883;" >{len(self.comments)}</span>
                    </span>
                    """,
                    unsafe_allow_html=True
                )

                for idx, comment in enumerate(self.comments, 1):
                    st.write(f"Comment {idx}: {Text_Cleaning(comment.strip())}")

                st.text("")

                self.download_comments = "\n\n".join(map(str, set(self.comments)))

                if __name__=="__main__":
                    download_text(  ### cownloading comments
                        text=Text_Cleaning(self.download_comments),
                        filename="comments.doc"
                    )
                    
                st.text("")
                st.text("")
                st.write("---")

        except Exception as e:
            return e
        


    ### scraping code tag
    def Scrap_codes(self)->any:
        """
        scraping all codes of 
        programing language  
        """

        try:
            self.language_codes = [] ### code list

            for i in self.soup.find_all("code"):
                self.language_codes.append(i.text)

            if len(self.language_codes)>0:
                st.markdown(
                    """
                    <h4 style="color: orangered;">
                        Codes 
                    </h4>
                    """,unsafe_allow_html=True)
                
                st.markdown(
                    f"""
                    <span>
                        Scraped Codes: <span style="color: #42b883;" >{len(self.language_codes)}</span>
                    </span>
                    """,
                    unsafe_allow_html=True
                )
                st.text("")
                for j in self.language_codes:
                    st.code(j,language="",line_numbers=True)
                    st.text("")
                    st.text("")

                st.text("")

                self.download_code = "\n\n".join(map(str, self.language_codes))

                if __name__=="__main__":
                    download_text(
                        text=self.download_code,
                        filename="codes.doc"
                    )
                st.text("")
                st.write("---")
        
        except Exception as er:
            return er
        

    ### scraping images
    def Scrap_All_images(self)->any:
        """
        scraping images img tag
        it containes svg images,
        img images , gifs,etc
        """

        try:
            self.image_src_link = []  ### list of src links

            for i in self.soup.find_all("img"):
                self.src_link = i.get("src")

                ### checking src starts with https://
                if self.src_link and self.src_link.startswith('https://'):
                    self.image_src_link.append(
                        self.src_link
                    )

            if len(self.image_src_link) > 0:
                

                ### creating 2 columns
                self.image_col1 = self.image_src_link[0::2]
                self.image_col2 = self.image_src_link[1::2]

                st.markdown(
                    """
                    <h4 style="color: orangered;">
                        Images 
                    </h4>
                    """,unsafe_allow_html=True)
                st.text("")

                st.markdown(
                    """
                    <h5>
                        jpg/png images 
                    </h5>
                    """,unsafe_allow_html=True
                )

                st.text("")

                image_column1,  image_column2 = st.columns(2,gap="small")
                
                ### displaying jpg and png images
                with image_column1:

                    try:
                        for  image_index , image in enumerate(self.image_col1,1):
                            download_image(
                                url=image,filename=f"Image-{str(image_index)}.png"
                            )
                            st.text("")
                    except Exception as er:
                        st.warning(f"Error...\n{er}",icon="⚠️")

                with image_column2:

                    try:
                        for image_index, image in enumerate(self.image_col2, 1):
                            download_image(
                                url=image,
                                filename=f"Image-{str(image_index)}.png"
                            )
                            st.text("")

                    except Exception as er:
                        st.warning(f"Error...\n{er}",icon="⚠️")

                st.text("")
                st.write("---")

            
            self.svg_image = [] ### list of svg images

            for i in self.soup.find_all("svg"):
                self.svg_image.append(i)

            if len(self.svg_image) > 0:
                self.svg_image_col1 = self.svg_image[0::2]
                self.svg_image_col2 = self.svg_image[1::2]

                st.text("")
                st.markdown(
                    """
                    <h4 style="color: orangered;">
                        Images 
                    </h4>
                    """,unsafe_allow_html=True)
                st.text("")
                st.markdown(
                    """
                    <h5>
                        svg images 
                    </h5>
                    """,unsafe_allow_html=True)
                
                svg_column1, svg_column2 = st.columns(2,gap="small")

                with svg_column1:
                    try:
                    ### displaying svg image
                        for image in self.svg_image_col1:
                            st.markdown(
                                str(image),
                                unsafe_allow_html=True
                            )
                    except Exception as err:
                        st.warning(f"Error...\n{err}",icon="⚠️")
                with svg_column2:
                    try:
                        ### displaying svg image
                        for image in self.svg_image_col2:
                            st.markdown(
                                str(image),
                                unsafe_allow_html=True
                            )

                    except Exception as er:
                        st.warning(f"Error...\n{er}",icon="⚠️")

                st.text("")
                st.write("---")

        except Exception as e:
            return e


    ### scraping videos    
    def Scrap_videos(self):
        """
        scraping videos src links
        present in video tag
        """ 
        try:
            self.video_link = []   ### src video links

            self.find_video = self.soup.find_all("video")   

            for i in self.find_video:
                self.source_tag = i.find("source")

                if self.source_tag:
                    self.video_link.append(
                        self.source_tag.get("src")
                    )

            
            if len(self.video_link) > 0:
                st.text("")
                st.markdown(
                        """
                        <h4 style="color: orangered;">
                            Videos 
                        </h4>
                        """,unsafe_allow_html=True)
                st.text("")

                self.video_link_col1 = self.video_link[0::2]
                self.video_link_col2 = self.video_link[1::2]

                video_link_column1, video_link_column2 = st.columns(2,gap="small")

                with video_link_column1:
                    try:
                        
                        for video in self.video_link_col1:
                            self.video_format1 = re.sub(r'.*?(https://)', r'\1', video) 
                            st.video(data=self.video_format1)

                    except Exception as err:
                        st.warning(f"Error...\n{err}",icon="⚠️")

                with video_link_column2:
                    try:
                        
                        for video in self.video_link_col2:
                            self.video_format2 = re.sub(r'.*?(https://)', r'\1', video) 
                            st.video(data=self.video_format2)

                    except Exception as err:
                        st.warning(f"Error...\n{err}",icon="⚠️")

            ############

            self.video_src_links = [] ## list of src video links

            for i in self.soup.find_all("video"):
                self.video_src_links.append(i.get('src'))    

            if len(self.video_src_links) > 0:

                self.video_src_link_col1 = self.video_src_links[0::2]
                self.video_src_link_col2 = self.video_src_links[1::2]

                video_src_link_column1, video_src_link_column2 = st.columns(2,gap="small")

                with video_src_link_column1:
                    try:
                        for video in self.video_src_link_col1:
                            self.src_video_format = re.sub(r'.*?(https://)', r'\1', video)
                            st.video(data=str(self.src_video_format))

                    except Exception as err:
                        st.warning(f"Error...\n{err}",icon="⚠️")
        
                with video_src_link_column2:
                    try:
                        for video in self.video_src_link_col2:
                            self.src_video_format1 = re.sub(r'.*?(https://)', r'\1', video)
                            st.video(data=str(self.src_video_format1))

                    except Exception as err:
                        st.warning(f"Error...\n{err}",icon="⚠️")

                st.text("")
                st.text("")
                st.write("---")
        
        except Exception as er:
            return er
            
    
    ### callink all methods
    def Display_all_elements(self,Input_url):

        try:
            self.Input_url = Input_url
            
            if __name__=="__main__":
                self.Scrap_All_Paragraph()

            if __name__=="__main__":
                self.Scrap_All_Heading()

            if __name__=="__main__":
                self.Scrap_All_links()

            if __name__=="__main__":
                self.Scrap_All_list()

            if __name__=="__main__":
                try:
                    self.Scrap_All_tables(Input_url)
                except :
                    pass

            if __name__=="__main__":
                self.Scrap_codes()

            if __name__=="__main__":
                self.Scrap_All_images()
                
            if __name__=="__main__":
                self.Scrap_videos()
                
            if __name__=="__main__":
                self.Scrap_All_text()
            
            if __name__=="__main__":
                self.Scrap_Span_text()
             
            if __name__=="__main__":
                self.Scrap_Div_text()
            
            if __name__=="__main__":
                self.Scrap_Comments()
            

        except Exception as e:
            return e



### advance scraper
class AdvanceScraper(WebScraper):


    ### number of paragraph selected 
    def Scrap_number_Paragraph(self,limit_paragraph):
        """
        scrap paragraph at a 
        limin or the value set in slider
        """

        try:
            self.Paragraph_list = []  ### list containing paragraphs

            self.limit_paragraph = limit_paragraph

            for i in self.soup.find_all("p"):
                self.Paragraph_list.append(Text_Cleaning(i.text))

            if len(self.Paragraph_list) <= limit_paragraph:
                limit_paragraph = len(self.Paragraph_list)

            if len(self.Paragraph_list) > 0:
                st.markdown(
                """
                <h4 style="color: orangered;">
                    Paragraphs
                </h4>
                """,unsafe_allow_html=True)
            
                st.markdown(
                        f"""
                        <span>
                            Total Paragraph: <span style="color: #42b883;" >{len(self.Paragraph_list)}</span>
                        </span>
                        <br>
                        <span>
                            Scraped Paragraph: <span style="color: #42b883;" >{str(limit_paragraph)}</span>
                        </span>
                        """,
                        unsafe_allow_html=True
                    )
                st.text("")
                st.text("")

                self.paragraph_amount = [] ### list containing the amount of paragraph scraped

                ### displaying paragraph
                for para in self.Paragraph_list[:limit_paragraph]:
                    self.paragraph_amount.append(para)
                    st.write(para)

                st.text("")

                self.para_amount_download = "\n\n".join(map(str, self.paragraph_amount))

                if __name__=="__main__": ### downloading paragraph
                    download_text(
                        text=self.para_amount_download,
                        filename="paragraph.doc"
                    )

                st.text("")
                st.write("---")

        except Exception as e:
            return e


       
### page setting 
st.set_page_config(
    page_title="web scraper",
    layout="wide",
    page_icon="🕸️",
    initial_sidebar_state="collapsed"
)

### app main css
if __name__=="__main__":
    insert_css("cssfiles/app.css")


### app side bar
App_sidebar = st.sidebar

with App_sidebar:
    st.text("")
    st.text("")
    st.subheader("Web Scraper 🌐")
    st.text("")

    #### navigation menu
    Main_menu = option_menu(
        menu_title="",
        options=["Web Scraper", "App Info"],
        default_index=0,
        icons=["browser-edge","person-circle"],
        key="Navigation Menu"
    )

    st.text("")

    project_link = """
        <a 
            href="https://github.com/Nishant43S/Web-Data-Scraper.git"
            style="text-decoration: none;"
            target="_blank">
            <button class="btn">Project link</button>
        </a>
    """

    ### project link button
    st.markdown(
        project_link,
        unsafe_allow_html=True
    )
    
    if __name__=="__main__":
        insert_css("cssfiles/project-link-btn.css")



# Function to zip the downloaded website folder
def zip_directory(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))




# Function to download the website and zip it, returning the zip file path
@st.cache_data(show_spinner=False)
def download_and_zip_website(url):
    # Create a directory to save the websites if it doesn't exist
    base_folder = "webdata"
    os.makedirs(base_folder, exist_ok=True)

    # Create a timestamped subfolder for each website
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    download_folder = os.path.join(base_folder, f"website_{timestamp}")
    os.makedirs(download_folder, exist_ok=True)

    # Set up PyWebCopy options
    kwargs = {'bypass_robots': True, 'project_name': 'website_copy'}
    
    try:
        # Download the website
        save_website(url, download_folder, **kwargs)
        
        # Zip the downloaded website folder
        zip_file_path = f"{download_folder}.zip"
        zip_directory(download_folder, zip_file_path)
        
        return zip_file_path
    
    except Exception as e:
        return f"Error downloading website: {e}"




### app section
if Main_menu == "Web Scraper":

    ### app column and blank column
    Blank_col1, App_Column, Blank_col2 = st.columns([2,8,2],gap="small")

    with Blank_col1:
        pass
    with Blank_col2:
        pass

    ### app column
    with App_Column:

        ### app heading
        App_Heading = colored_header(
            label="Web Scraper📑",
            description="Scrap Website Data",
            color_name="violet-70"
        )

        ### taking user input
        Url_input = st.text_input(
            label="Paste Url",
            label_visibility="visible",
            placeholder="https://www.example.com",
            type="default"
        )


        ### button and advance mode column
        Button_col, Advance_mode_col, Blank_btn_col = st.columns([4,4,11],gap="small")

        with Blank_btn_col:
            pass

        with Button_col:

            ### scrap button
            Scrap_website_btn = st.button(
                label="Scrap Website",
                key="Scrap Button"
            )
        
        with Advance_mode_col:

            ### toggle button for switching advance mode
            Advance_mode = st.toggle(
                label="Advance Mode",
                label_visibility="visible",
                value=False,
                key="Advance mode"
            )

        if Advance_mode:
            st.toast("advance mode",icon="🕸️")
            try:
                if Url_input.strip() != "":
                    ### creating expander of advance mode
                    advance_mode_expander = st.expander(label="Advance Scraper Mode",expanded=True,icon="🪓")

                    with advance_mode_expander:
                        
                        ### check bos to select  paragraph
                        Paragraph_checkbox = st.checkbox(
                            label="Scrap Website paragraphs",
                            value=True,key="Paragraph check box"
                        )

                        if Paragraph_checkbox:
                            
                            ### paragraph selector
                            Para_slider = st.slider(
                                label="Number Of Paragraph",
                                max_value=100,min_value=1,
                                step=1,key="number of paragraph",
                                value=10
                            )

                        st.write("Basic html Elements for scraping")

                        ### creating columns for checkbox
                        advance_col1, advance_col2, advance_col3 = st.columns(3,gap="small")   

                        st.text("")
                        with advance_col1:

                            ### heading checkbos
                            Heading_checkbox = st.checkbox(
                                label="Headings h1 - h6",
                                value=True,
                                label_visibility="visible",
                                key="Website headings"
                            )

                        with advance_col2:

                            ### Links checkbox
                            Link_checkbox = st.checkbox(
                                label="All Website links",
                                value=False,
                                key="Links of website",
                                label_visibility="visible"
                            )
                        
                        with advance_col3:

                            ### List checkbox
                            List_checkbox = st.checkbox(
                                label="Website Lists",
                                value=False,
                                key="Lists of website",
                                label_visibility="visible"
                            )

                        with advance_col1:
                            
                            ### table checkbox
                            Table_checkbox = st.checkbox(
                                label="Website Tables",
                                value=False,
                                key="Tables of website",
                                label_visibility="visible"
                            )

                        with advance_col2:
                                
                            ### code checkbox
                            Code_checkbox = st.checkbox(
                                label="Programing language codes",
                                value=False,
                                key="code of programing of website",
                                label_visibility="visible"
                            )

                        with advance_col3:
                            
                            ### video checkbox
                            Video_checkbox =  st.checkbox(
                                label="Website Videos",
                                value=False,
                                key="videos of website",
                                label_visibility="visible"
                            )

                        with advance_col1:

                            ### images checkbox
                            Image_checkbox =  st.checkbox(
                                label="Website Images png/jpg",
                                value=False,
                                key="Images of website",
                                label_visibility="visible"
                            )

                        with advance_col2:

                            ### scrap all text
                            All_text_checkbox =  st.checkbox(
                                label="Website all text",
                                value=False,
                                key="Extra text of website",
                                label_visibility="visible"
                            )

                        # st.write("---")
                        with advance_col3:

                            ### scrap span tag all text
                            Span_text_checkbox =  st.checkbox(
                                label="Website all span text",
                                value=False,
                                key="Span tag text of website",
                                label_visibility="visible"
                            )
                        
                        with advance_col1:

                            ### scrap all div tag text
                            Div_text_checkbox =  st.checkbox(
                                label="Website all div text",
                                value=False,
                                key="div tag text of website",
                                label_visibility="visible"
                            )
                        with advance_col2:

                            ### scrap all div tag text
                            Comments_checkbox =  st.checkbox(
                                label="Scrap Website Comments",
                                value=False,
                                key="Comments of website",
                                label_visibility="visible"
                            )
                        
             
                        st.markdown("<hr style='margin: 0; padding: 0;'>",unsafe_allow_html=True)

                        Download_websitecol1, Download_websitecol2,Download_websitecol3 = st.columns(3,gap="small")

                        with Download_websitecol3:
                            pass

                        ### download website toggle button
                        with Download_websitecol1:

                            Download_link_toggle = st.toggle(
                                label="Generate download link",
                                value=False,label_visibility="visible",
                                key="Download website source code"
                            )

                        with Download_websitecol2:
                                                        
                            # When the button is pressed, download, zip, and provide download link
                            if Download_link_toggle:
                                if Url_input:
                                    with st.spinner("Generating link..."):
                                        # Call the function to download and zip the website
                                        zip_path = download_and_zip_website(Url_input)
                                        
                                        # If download was successful, provide the file for download
                                        if zip_path.endswith('.zip'):
                                            st.toast("Website download link generated")
                                            
                                            # Provide a download button for the zipped file
                                            with open(zip_path, 'rb') as file:
                                                st.download_button(
                                                    label="Download Website Source code",
                                                    data=file,
                                                    file_name=os.path.basename(zip_path),
                                                    mime='application/zip',
                                                    use_container_width=True
                                                )
                                        else:
                                            st.toast(zip_path)  # Show error message if something went wrong
                                else:
                                    st.toast("Please enter a valid URL")


            except :
                pass


            if Url_input.strip() != "":
                advace_scraper = AdvanceScraper(Url_input)  ### advance scraper object


                try:

                    with st.spinner("Generating..."):

                        ### if paragraph checkbox clicked
                        if Paragraph_checkbox:
                            st.toast("Paragraphs Scraped",icon="📄")
                            if __name__=="__main__":
                                st.session_state.paragraph = advace_scraper.Scrap_number_Paragraph(Para_slider)

                                if "paragraph" in st.session_state:
                                    paragraph = st.session_state.paragraph
                                    
                        ## if headings checkbox clicked
                        if Heading_checkbox:
                            st.toast("Headings Scraped",icon="📑")
                            if __name__=="__main__":
                                advace_scraper.Scrap_All_Heading()

                        ## if links checkbox clicked
                        if Link_checkbox:
                            st.toast("Links Scraped",icon="🌐")
                            if __name__=="__main__":
                                advace_scraper.Scrap_All_links()

                        ## if list checkbox clicked
                        if List_checkbox:
                            st.toast("List Scraped",icon='📜')
                            if __name__=="__main__":
                                advace_scraper.Scrap_All_list()
                        
                        ### if table checkbox clicked
                        if Table_checkbox:
                            if __name__=="__main__":
                                try:
                                    advace_scraper.Scrap_All_tables(Url_input)
                                except:
                                    pass
                        
                        ### if checkbox clicked
                        if Code_checkbox:
                            if __name__=="__main__":
                                advace_scraper.Scrap_codes()
                        
                        ### if checkbox clicked
                        if Video_checkbox:
                            if __name__=="__main__":
                                advace_scraper.Scrap_videos()
                        
                        ### if checkbox clicked
                        if Image_checkbox:
                            st.toast("Images Scraped",icon="📸")
                            if __name__=="__main__":
                                advace_scraper.Scrap_All_images()

                        ### if checkbox clicked
                        if All_text_checkbox:
                            st.toast("All text Scraped",icon="📰")
                            if __name__=="__main__":
                                advace_scraper.Scrap_All_text()
                        
                        ### if checkbox clicked
                        if Span_text_checkbox:
                            st.toast("All Span text Scraped",icon="📄")
                            if __name__=="__main__":
                                advace_scraper.Scrap_Span_text()

                        ### if checkbox clicked
                        if Div_text_checkbox:
                            st.toast("All Div text Scraped",icon="📄")
                            if __name__=="__main__":
                                advace_scraper.Scrap_Div_text()
                        
                        ### if checkbox clicked
                        if Comments_checkbox:
                            st.toast("All Comments Scraped",icon="📑")
                            if __name__=="__main__":
                                advace_scraper.Scrap_Comments()
                        
                        
                        CheckBox_list = [
                            Paragraph_checkbox, Heading_checkbox,
                            List_checkbox, Link_checkbox, Table_checkbox,
                            Code_checkbox, Video_checkbox, Image_checkbox,
                            All_text_checkbox, Span_text_checkbox,
                            Div_text_checkbox, Comments_checkbox
                        ]

                        if not any(CheckBox_list):
                            st.info("Select any checkbox",icon="☑️") 

                except:
                    st.warning("Select any option",icon='')
            else:
                st.warning("please enter url",icon="✏️")

        else:
            if Scrap_website_btn:
                if Url_input.strip() != "":
                    
                    ### scraper object
                    scraper = WebScraper(Url_input)

                    ### displaying web content
                    with st.spinner("Generating..."):
                        scraper.Display_all_elements(Url_input)
                    
                else:
                    st.warning("please enter url",icon="✏️")


        if Url_input.strip() == "":

            ### lottie animations
            Web_animation1, Web_animation2 = st.columns(2,vertical_alignment="center")

            with Web_animation1:

                try:
                    Web_developement_1 = insert_lottie_animation("lottie_animations/Web-developement-1.json")
                    st_lottie(
                        animation_source=Web_developement_1,
                        speed=1,
                        reverse=False,loop=True,
                        quality="high",
                        height=365,
                        width=425,
                        key="web animation"
                    )

                except Exception as err:
                    st.warning("something went wrong...",err,icon="⚠️")

            with Web_animation2:    
                    
                try:
                    Data_loading_animation = insert_lottie_animation("lottie_animations/data-loading.json")
                    st_lottie(
                        animation_source=Data_loading_animation,
                        speed=1,
                        reverse=False,loop=True,
                        quality="high",
                        height=365,
                        width=410,
                        key="ploading data"
                    )
                    
                except Exception as err:
                    st.warning("something went wrong...",err,icon="⚠️")


### app info
if Main_menu == "App Info":

    ### creating columns
    Blank_appinfo1, App_info_col, Blank_appinfo2 = st.columns(
        [2,8,2],gap="small"
    )

    ### blank app info column
    with Blank_appinfo1:
        pass

    with Blank_appinfo2:
        pass
    
    ### app info column
    with App_info_col:
    
        ### adding external html file
        if __name__=="__main__":
            st.markdown(
                insert_html("htmlfile/about-app.html"),
                unsafe_allow_html=True
            )

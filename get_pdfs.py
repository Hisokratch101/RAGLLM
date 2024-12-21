import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import time

class ArticleScraper:
    def __init__(self, base_url="https://ardna.org"):
        self.base_url = base_url
        self.session = requests.Session()
        # Create a directory for downloads if it doesn't exist
        self.download_dir = "downloaded_pdfs"
        os.makedirs(self.download_dir, exist_ok=True)

    def get_article_urls(self, main_page_html):
        """Extract article URLs from the main page"""
        soup = BeautifulSoup(main_page_html, 'html.parser')
        article_links = []
        
        # Find all article links - they have the pattern /articles/detail?id=XX
        for link in soup.find_all('a', href=True):
            if '/articles/detail?id=' in link['href']:
                full_url = urljoin(self.base_url, link['href'])
                article_links.append(full_url)
        
        return article_links

    def get_pdf_url(self, article_page_html):
        """Extract PDF URL from an article detail page if it exists"""
        soup = BeautifulSoup(article_page_html, 'html.parser')
        
        # Look for PDF links in the specific card structure
        pdf_link = soup.find('a', href=lambda x: x and '.pdf' in x.lower())
        if pdf_link:
            return pdf_link['href']
        return None

    def download_pdf(self, pdf_url, article_title):
        """Download the PDF file"""
        try:
            response = self.session.get(pdf_url, stream=True)
            if response.status_code == 200:
                # Clean filename from article title
                filename = f"{article_title.replace('/', '_')}.pdf"
                filepath = os.path.join(self.download_dir, filename)
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"Successfully downloaded: {filename}")
                return True
            else:
                print(f"Failed to download PDF from {pdf_url}")
                return False
        except Exception as e:
            print(f"Error downloading PDF: {str(e)}")
            return False

    def scrape_articles(self, main_page_html):
        """Main function to scrape articles and download PDFs"""
        article_urls = self.get_article_urls(main_page_html)
        print(f"Found {len(article_urls)} articles to process")

        for article_url in article_urls:
            try:
                print(f"\nProcessing article: {article_url}")
                
                # Get the article page
                response = self.session.get(article_url)
                if response.status_code != 200:
                    print(f"Failed to fetch article page: {article_url}")
                    continue

                # Extract article title for filename
                soup = BeautifulSoup(response.text, 'html.parser')
                title_elem = soup.find('h1')
                article_title = title_elem.text.strip() if title_elem else f"article_{article_url.split('=')[-1]}"

                # Get PDF URL if it exists
                pdf_url = self.get_pdf_url(response.text)
                if pdf_url:
                    print(f"Found PDF: {pdf_url}")
                    self.download_pdf(pdf_url, article_title)
                else:
                    print("No PDF found in this article")

                # Be nice to the server
                time.sleep(1)

            except Exception as e:
                print(f"Error processing article {article_url}: {str(e)}")
                continue

def main():
    scraper = ArticleScraper()
    
    # You would pass the main page HTML here
    main_page_html = """
<!doctype html>
<!--dir="rtl"-->
<html lang="en">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="shortcut icon" href="https://ardna.org/dist/img/favicon1.png" type="image/x-icon">



    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://ardna.org/assets/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://ardna.org/assets/bootstrap/css/bootstrap-select.min.css">
    <!-- icon css-->
    <link rel="stylesheet" href="https://ardna.org/assets/font-awesome/css/all.css">
    <link rel="stylesheet" href="https://ardna.org/assets/elagent-icon/style.css">
    <link rel="stylesheet" href="https://ardna.org/assets/niceselectpicker/nice-select.css">
    <link rel="stylesheet" href="https://ardna.org/assets/animation/animate.css">
    <link rel="stylesheet" href="https://ardna.org/assets/prism/prism.css">
    <link rel="stylesheet" href="https://ardna.org/assets/prism/prism-coy.css">
    <link rel="stylesheet" href="https://ardna.org/assets/mcustomscrollbar/jquery.mCustomScrollbar.min.css">
    <link rel="stylesheet" href="https://ardna.org/assets/thdoan-magnify/css/magnify.css">
    <link rel="stylesheet" href="https://ardna.org/dist/css/style.css">
    <link rel="stylesheet" href="https://ardna.org/dist/css/responsive.css">


        <!-- GOOGLE FONT CSS -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Almarai&display=swap" rel="stylesheet">

    <!-- RTL CSS -->
    <link rel="stylesheet" href="https://ardna.org/dist/css/rtl.css">
    
    <title>ARDNA</title>

    <script type="text/javascript"
        src="https://platform-api.sharethis.com/js/sharethis.js#property=60e789069804b500190921af&product=inline-share-buttons"
        async="async"></script>
</head>

<body data-scroll-animation="true">

    <div id="preloader">
    <div id="ctn-preloader" class="ctn-preloader">
        <div class="round_spinner">
            <div class="spinner"></div>
            <div class="text">
                <img src="https://ardna.org/dist/img/spinner_logo.png" alt="">
            </div>
        </div>
        <h2 class="head">قاعدة المعرفة الفلاحية</h2>
        <p class="wow fadeInUp" data-wow-delay="0.5s">ما هي المعلومات التي تبحث عنها؟         </p>
    </div>
</div>
    <div class="body_wrapper">

         <!--<nav class="navbar menu_two" style="background-color: #7abf4bad;">
     <div class="container">
         <a class="navbar-brand" href="/" style="color: #fff;font-size: 14px;font-weight: 500;">
             KNOWLEDGE BASE
         </a>
         <a class="navbar-brand" href="/" style="color: #fff;font-size: 14px;font-weight: 500;">
             FACE AGRI
         </a>
         <a class="navbar-brand" href="/" style="color: #fff;font-size: 14px;font-weight: 500;">
             FFS
         </a>
         <a class="navbar-brand" href="/" style="color: #fff;font-size: 14px;font-weight: 500;">
             E-LEARNIING
         </a>
     </div>
 </nav> style="top:38px!important"-->

 

 <nav class="navbar navbar-expand-lg menu_two" id="sticky">
     <div class="container">
         <a class="navbar-brand" href="https://ardna.org/">
             <img src="https://ardna.org/dist/img/onca.png"
                 srcset="https://ardna.org/dist/img/onca-2x.png 2x" alt="logo" style="width:30%">
             <img src="https://ardna.org/dist/img/logo.png"
                 srcset="https://ardna.org/dist/img/logo-2x.png 2x" alt="logo" style="width:25%">

         </a>
         <button class="navbar-toggler collapsed" type="button" data-toggle="collapse"
             data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
             aria-label="Toggle navigation">
             <span class="menu_toggle">
                 <span class="hamburger">
                     <span></span>
                     <span></span>
                     <span></span>
                 </span>
                 <span class="hamburger-cross">
                     <span></span>
                     <span></span>
                 </span>
             </span>
         </button>


         <div class="collapse navbar-collapse" id="navbarSupportedContent">
             <ul class="navbar-nav menu dk_menu ml-auto">
                 <li class="nav-item dropdown submenu active">
                     <a href="https://ardna.org//basedesconnaissnances"
                         class="nav-link dropdown-toggle" role="button" data-toggle="dropdown" aria-haspopup="true"
                         aria-expanded="false">الصفحة الرئيسية</a>
                     <i class="arrow_carrot-down_alt2 mobile_dropdown_icon" aria-hidden="true"
                         data-toggle="dropdown"></i>
                 </li>
                 <li class="nav-item dropdown submenu">
                     <a class="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown"
                         aria-haspopup="true" aria-expanded="false">
                         المحاور                     </a>
                     <i class="arrow_carrot-down_alt2 mobile_dropdown_icon" aria-hidden="false"
                         data-toggle="dropdown"></i>
                     <ul class="dropdown-menu">
                         
                         <li class="nav-item ">
                             <a href="https://ardna.org//articles/thematiques?id=1"
                                 class="nav-link">المسار التقني لسلاسل الإنتاج&#8230;</a>
                         </li>

                         
                         <li class="nav-item ">
                             <a href="https://ardna.org//articles/thematiques?id=3"
                                 class="nav-link">ريادة الأعمال للفلاحين الشباب&#8230;</a>
                         </li>

                         
                         <li class="nav-item ">
                             <a href="https://ardna.org//articles/thematiques?id=4"
                                 class="nav-link">مواجهة تغير المناخ /&#8230;</a>
                         </li>

                         
                         <li class="nav-item ">
                             <a href="https://ardna.org//articles/thematiques?id=2"
                                 class="nav-link">التثمين والتسويق / التحفيزات&#8230;</a>
                         </li>

                                              </ul>
                 </li>
                 <li class="nav-item dropdown submenu">
                     <a class="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown"
                         aria-haspopup="true" aria-expanded="false">
                         الفئات                     </a>
                     <i class="arrow_carrot-down_alt2 mobile_dropdown_icon" aria-hidden="false"
                         data-toggle="dropdown"></i>
                     <ul class="dropdown-menu">
                         
                         <li class="nav-item ">
                             <a href="https://ardna.org//articles/categories?id=3"
                                 class="nav-link">مقالات و بحوث   </a>
                         </li>

                         
                         <li class="nav-item ">
                             <a href="https://ardna.org//articles/categories?id=6"
                                 class="nav-link">برامج اذاعية</a>
                         </li>

                         
                         <li class="nav-item ">
                             <a href="https://ardna.org//articles/categories?id=2"
                                 class="nav-link">دليل المماراسات الجيدة</a>
                         </li>

                         
                         <li class="nav-item ">
                             <a href="https://ardna.org//articles/categories?id=5"
                                 class="nav-link">المدونة الصوتية</a>
                         </li>

                         
                         <li class="nav-item ">
                             <a href="https://ardna.org//articles/categories?id=1"
                                 class="nav-link">التقارير والمنشورات</a>
                         </li>

                         
                         <li class="nav-item ">
                             <a href="https://ardna.org//articles/categories?id=4"
                                 class="nav-link">أشرطة فيديو / كتيبات رقمية</a>
                         </li>

                                              </ul>
                 </li>
                 <li class="nav-item dropdown submenu">
                     <a class="nav-link dropdown-toggle"
                         href="https://ardna.org//articles/contacternous" role="button"
                         data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                         شركاءنا                      </a>
                     <i class="arrow_carrot-down_alt2 mobile_dropdown_icon" aria-hidden="false"
                         data-toggle="dropdown"></i>
                 </li>
                 <li class="nav-item dropdown submenu">
                     <a class="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown"
                         aria-haspopup="true" aria-expanded="false">
                         اللغة
                     </a>
                     <i class="arrow_carrot-down_alt2 mobile_dropdown_icon" aria-hidden="false"
                         data-toggle="dropdown"></i>
                     <ul class="dropdown-menu">
                         <li class="nav-item ">
                             <a href="/fr/basedesconnaissnances" class="nav-link">الفرنسية</a>
                         </li>
                         <li class="nav-item ">
                             <a href="/basedesconnaissnances" class="nav-link">العربية</a>
                         </li>
                     </ul>
                 </li>
             </ul>
             <!--<a class="nav_btn" href="signin.html"><i class="icon_profile"></i>Log In</a>-->
         </div>
     </div>
 </nav>
        <section class="doc_documentation_area" id="sticky_doc">
    <!-- <div class="overlay_bg"></div> -->
    <div class="container custom_container">
        <div class="row">
            <div class="col-lg-3 doc_mobile_menu">
    <aside class="doc_left_sidebarlist">
        <div class="open_icon" id="left">
            <i class="arrow_carrot-right"></i>
            <i class="arrow_carrot-left"></i>
        </div>
        <div class="scroll">
            <ul class="list-unstyled nav-sidebar">
                                <li class="nav-item">
                    <a href="#" class="nav-link">
                        <img src="https://ardna.org/dist/img/side-nav/chat1.png"
                            alt="">الفئات                    </a>
                    <span class="icon"><i class="arrow_carrot-down"></i></span>
                    <ul class="list-unstyled dropdown_nav">
                                                <li><a href="/articles/categories?id=3">
                                                                مقالات و بحوث                                                               </a>

                        </li>
                                                <li><a href="/articles/categories?id=6">
                                                                برامج اذاعية                                                            </a>

                        </li>
                                                <li><a href="/articles/categories?id=2">
                                                                دليل المماراسات الجيدة                                                            </a>

                        </li>
                                                <li><a href="/articles/categories?id=5">
                                                                المدونة الصوتية                                                            </a>

                        </li>
                                                <li><a href="/articles/categories?id=1">
                                                                التقارير والمنشورات                                                            </a>

                        </li>
                                                <li><a href="/articles/categories?id=4">
                                                                أشرطة فيديو / كتيبات رقمية                                                            </a>

                        </li>
                        
                    </ul>
                </li>
                <li class="nav-item active">
                    <a href="#" class="nav-link">
                        <img src="https://ardna.org/dist/img/side-nav/document.png"
                            alt="">المحاور                    </a>
                    <span class="icon"><i class="arrow_carrot-down"></i></span>
                    <ul class="list-unstyled dropdown_nav">
                                                <li><a
                                href="/articles/thematiques?id=1">
                                                                المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                                            </a>

                        </li>
                                                <li><a
                                href="/articles/thematiques?id=3">
                                                                ريادة الأعمال للفلاحين الشباب والمرأة القروية / التننظيمات المهنية                                                            </a>

                        </li>
                                                <li><a
                                href="/articles/thematiques?id=4">
                                                                مواجهة تغير المناخ / برامج اقتصاد المياه / الزرع المباشر /  الترحال                                                            </a>

                        </li>
                                                <li><a
                                href="/articles/thematiques?id=2">
                                                                التثمين والتسويق / التحفيزات والمساعدات المقدمة من طرف الدولة / التمليك / الترميز                                                            </a>

                        </li>
                                            </ul>
                </li>
            </ul>
        </div>
    </aside>
</div>                        <div class="col-lg-9 col-md-8">
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=40">دليل الفلاح تربية الأغنام سلالة بني كيل</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-04-14                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=41">دليل الفلاح تربية الماعز الحلوب</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2023-03-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=42">دليل الفلاح - الزراعة بالملقحات البرية (فاب) كيفية حماية الملقحات البرية والاستفادة من خدماتها</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=43">دليل الفلاح- زراعة الفويلة</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=47">دليل الفلاح زراعة الزيتون الأمراض والآفات</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=48">دليل الفلاح تربية الأرانب ورعايتها</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=50">دليل الفلاح زراعة الحوامض</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=51">دليل الفلاح شجرة اللوز</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=52">دليل الفلاح زراعة القمح</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=53">دليل الفلاح تربية النحل</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=55">دليل الفلاح تربية الإبل</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=56">دليل الفلاح شجرة التين</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=57">دليل الفلاح زراعة توت الأرض</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=58">دليل الفلاح زراعة نخيل التمر</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=59">دليل الفلاح زراعة التفاح</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=60">دليل الفلاح زراعة الزعفران</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=61">دليل الفلاح تربية الأغنام سلالة السردي</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=133">دلیل المرشد الفلاحي لسلسلة المشمش</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=134">بطاقة تقنية مفصلة لسلسلة الحوامض</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=135"> وثيقة تقنية خاصة بسلسلة اللوز</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=136">دليل الفلاح: القمح الصلب، القمح اللين،  والشعير</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=137">دليل الفلاح لسلسلة القطاني الغذائية</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=138">دلیل المرشد الفلاحي لسلسلة القطاني الغذائية</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=139">دلیل الفلاح لسلسلة الخضروات </a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=140">دليل المرشد الفلاحي لسلسلة الخضراوات </a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=141">دليل المرشد الفلاحي للنباتات الزيتية</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=142">دليل الفلاح للنباتات الزيتية</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2023-03-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=143">دليل عملي خاص بالمستشارين الفلاحيين</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2023-03-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=144">دليل الفلاح للنباتات السكرية</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=145"> بطاقة تقنية مفصلة لسلسلة التين</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=146">وثيقة خاصة لسلسلة الحليب </a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=147">دلیل المرشد الفلاحي لسلسلة الجوز </a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=148">دلیل الفلاح لسلسلة الجوز </a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=149">  وثيقة تقنية خاصة بسلسلة الزيتون </a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=150">دلیل الفلاح لسلسلة الاجاص</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=151">دلیل المرشد الفلاحي لسلسلة الاجاص</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=152">بطاقة تقنية مفصلة لسلسلة التفاح</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=153">وثيقة خاصة لسلسلة اللحوم الحمراء (الماعز)</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=154">وثيقة خاصة لسلسلة اللحوم الحمراء (الاغنام)</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=155">دلیل الكساب لسلسلة لحوم الابقار</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=156">دلیل المرشد الفلاحي لسلسلة لحوم الابقار</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=157">دليل الفلاح لسلسلة العنب</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=158">دلیل المرشد الفلاحي لسلسلة العنب</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=159">دليل الفلاح لزراعة الحوامض</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=160">دليل الفلاح لشجرة اللوز</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=161">دليل الفلاح لتربية النحل</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=162">دليل الفلاح لزراعة القمح</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=163">دليل الفلاح لزراعة الكرز</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=164">دليل الفلاح لتربية الابل</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=165">دليل الفلاح لشجرة التين</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=166">دليل الفلاح لزراعة توت الارض</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-04-13                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=167">دليل الفلاح لزراعة نخيل التمر </a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=168">دليل الفلاح لزراعة التفاح</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=169">دليل الفلاح لزراعة الزعفران</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=170">دليل الفلاح لتربية الاغنام (سلاسلة السردي)</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=171">دليل الفلاح لنظام الزرع المباشر</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=172">دليل الفلاح لزراعة نوار الشمس</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=174">دليل الفلاح لشجرة الزيتون </a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=175">دليل الفلاح لتربية الاغنام (سلالة بني كيل)</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=176">دليل الفلاح لتربية الماعز الحلوب</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=177">دليل الفلاح : الزراعة بالملحقات البرية</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=178">دليل الفلاح لزراعة الفويلة</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=179">دليل الفلاح لزراعة الرمان</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=181">دليل الفلاح: زراعة الحبوب (الامراض و الافات)</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2023-03-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=182">دليل الفلاح لزراعة الزيتون : الامراض و الافات</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=183">دليل الفلاح: تربية الارانب و رعايتها</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2021-11-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=686">دليل الممارسات الجيدة لسلسلة اللوز</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-17                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=737">بطاقة تقنية مفصلة لسلسلة التفاح</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-03                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=761">  المراجع التقنية والتقنو-اقتصادية سلسلة الحليب</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-09                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=808">دليل الفلاح: زراعة الحوامض</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=811">دليل الفلاح : زراعة اللوز </a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=812">دليل الفلاح : تربية النحل</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=815">دليل الفلاح: زراعة الأفوكا</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=816">دليل الفلاح: تربية غنم سلالة بوجعد</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=817">دليل الفلاح: زراعة الشمندر السكري</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=818">دليل الفلاح : زراعة القرع الأخضر (الكورجيط)</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=819">دليل الفلاح: زراعة الصبار</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=820">دليل الفلاح: خسائر الحبوب عند الحصاد</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=821">دليل الفلاح: زراعة القمح</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=822">دليل الفلاح: تربية غنم سلالة الدمان</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=823">دليل الفلاح: تربية الحلزون</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=824">دليل الفلاح: تسمين العجول</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=825">دليل الفلاح: الزراعة باستخدام الملقحات البرية (فاب)</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        مواجهة تغير المناخ / برامج اقتصاد المياه / الزرع المباشر /  الترحال                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=826">دليل الفلاح: حليب النوق</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=827">دليل الفلاح: زراعة العدس</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=828">دليل الفلاح: زراعة الذرة العلفية</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=829"> دليل الفلاح: أمراض الحوامض</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=830">دليل الفلاح: زراعة البطيخ</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=831">دليل الفلاح: زراعة الزيتون</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=834">دليل الفلاح: تسمين الأغنام</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=835">دليل الفلاح: زراعة نخيل التمر</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=837">دليل الفلاح: زراعة ورد العطور</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=838">دليل الفلاح: زراعة البطيخ الأحمر</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=839">دليل الفلاح: زراعة الجلبانة</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-28                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=842">دليل الفلاح: زراعة الحمص</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=843">دليل الفلاح: زراعة البطاطس</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=845">دليل الفلاح: زراعة العنب</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=846">دليل الفلاح: زراعة البرقوق</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=847">دليل الفلاح: تربية غنم سلالة الصردي </a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-22                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=849">دليل الفلاح: سيلاج الذرة</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=850">دليل الفلاح: تربية غنم سلالة تمحضيت</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=851">دليل الفلاح: زراعة نوار الشمس</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=852">دليل الفلاح: تغذية الأبقار الحلوب</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-28                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=865">دليل الفلاح : زراعة التين</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=867">دليل الفلاح : زراعة توت الأرض</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=868">دليل الفلاح : زراعة  التفاح</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=869">دليل الفلاح : زراعة  الزعفران</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-28                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=871">دليل الفلاح : الزرع المباشر</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        مواجهة تغير المناخ / برامج اقتصاد المياه / الزرع المباشر /  الترحال                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-28                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=872">دليل الفلاح: تربية غنم سلالة بني كيل</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=873">دليل الفلاح : تربية الماعز الحلوب</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-28                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=874">دليل الفلاح : تربية الأرانب</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-24                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=883">دليل الفلاح : زراعة  الفويلة</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-28                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=884">دليل الفلاح : زراعة  الرمان</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-28                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=885">دليل الراعي</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        مواجهة تغير المناخ / برامج اقتصاد المياه / الزرع المباشر /  الترحال                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-28                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=886">دليل الفلاح: أمراض الحبوب</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-28                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=887">دليل الفلاح: أمراض الزيتون</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-28                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=889">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة المشمش: دلیل المستشار الفلاحي</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-28                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=894">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة الحوامض: بطاقة تقنية مفصلة</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-28                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=897">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة اللوز: بطاقة تقنية </a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-28                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=901">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة الحبوب: دليل الفلاح </a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-02-28                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=905">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة القطاني الغذائية: دليل المستشار الفلاحي</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-03-15                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=906">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة القطاني الغذائية: دليل الفلاح</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-03-02                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=918">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة الخضراوات: دليل المستشار الفلاحي</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-03-02                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=919">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة الخضراوات: دليل الفلاح</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-03-02                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=936">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة الزراعات السكرية: دليل الفلاح</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-03-16                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=1020"> المرجع التقني والتقنو-اقتصادي الخاص بسلسلة  التين: بطاقة تقنية مفصلة </a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-03-16                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=1039">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة  الحليب: بطاقة تقنية مفصلة</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-03-16                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=1041">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة  الزيتون: بطاقة تقنية مفصلة</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-03-16                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=1044">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة  التفاح : بطاقة تقنية مفصلة</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-05-20                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=1046">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة  اللحوم الحمراء للماعز : بطاقة تقنية مفصلة</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-05-26                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=1050">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة  اللحوم الحمراء للأغنام : بطاقة تقنية مفصلة</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-05-26                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=1060">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة الزراعات الزيتية: دليل الفلاح</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-05-25                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=1077">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة الجوز: دليل المستشار الفلاحي</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-05-25                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=1078">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة الجوز: دليل الفلاح</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-05-25                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=1090">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة الإجاص: دليل المستشار الفلاحي</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-05-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=1091">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة الإجاص: دليل الفلاح</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-05-25                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=1094">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة الزراعات الزيتية: دليل المستشار الفلاحي</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-05-25                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=1098">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة اللحوم الحمراء: دليل المستشار الفلاحي</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-05-26                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=1105">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة العنب: دليل المستشار الفلاحي</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-05-23                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=1106">المرجع التقني والتقنو-اقتصادي الخاص بسلسلة العنب هز على شكل دليل موجه للمستشلرين الفلاحيين وللفلاحين أو الراغبين في ممارسة زراعة العنب. </a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2022-04-26                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                                <div id="post" class="documentation_info">
                    <div class="community-post style-two improvement kbDoc open druid">
                        <div class="post-content">
                            <div class="author-avatar">
                                <img src="https://ardna.org/dist/img/categories/guide.png"
                                    alt="community post">
                            </div>
                            <div class="entry-content">
                                <h3 class="post-title" style="text-transform: uppercase;">
                                    <a
                                        href="/articles/detail?id=1795">دليل الفلاح نخيل التمر</a>
                                </h3>
                                <!--<div class="cat-wrap">
                                    <a class="badge" href="#">Articles</a>
                                </div>-->
                                <!--<span class="com-featured">
                                    <i class="icon_check"></i>
                                </span>-->
                                <ul class="meta">
                                    <li><a href="#">
                                                                                        المسار التقني لسلاسل الإنتاج / الفلاحة البيولوجية / الفلاحة التضامنية  و المنتجات المحلية                                            </a></li>
                                    <li><i class="icon_calendar"></i> Publié le
                                        2024-06-25                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="post-meta-wrapper">
                            <ul class="post-meta-info">
                                <li><a href="#">
                                                                                المكتب الوطني للاستشارة الفلاحية                                        </a></li>
                            </ul>
                        </div>
                    </div>


                </div>
                            </div>

        </div>
    </div>
</section>
        <footer class="footer_area f_bg_color">
    <img class="p_absolute leaf" src="https://ardna.org/dist/img/home_one/b_leaf.svg" alt="">
    <img class="p_absolute f_man wow fadeInLeft" data-wow-delay="0.4s"
        src="https://ardna.org/dist/img/home_two/f_man.png" alt="">
    <img class="p_absolute f_cloud" src="https://ardna.org/dist/img/home_two/cloud.png" alt="">
    <img class="p_absolute f_email" src="https://ardna.org/dist/img/home_two/email-icon.png" alt="">
    <img class="p_absolute f_email_two" src="https://ardna.org/dist/img/home_two/email-icon_two.png" alt="">
    <img class="p_absolute f_man_two wow fadeInLeft" data-wow-delay="0.2s"
        src="https://ardna.org/dist/img/home_two/man.png" alt="">
    <div class="footer_top">
        <div class="container">
            <div class="row">
                <div class="col-lg-4 col-sm-6">
                    <div class="f_widget subscribe_widget wow fadeInUp">
                        <a href="" class="f_logo"><img
                                src="https://ardna.org/dist/img/logo.png" alt=""></a>
                        <h4 class="c_head">اشترك في نشرتنا الإخبارية</h4>
                        <form action="#" class="footer_subscribe_form">
                            <input type="email" placeholder="Email" class="form-control">
                            <button type="submit" class="s_btn">أرسل</button>
                        </form>
                        <ul class="list-unstyled f_social_icon">
                            <li><a href="https://www.facebook.com/ONCAOFFICIEL"><i class="social_facebook"></i></a></li>
                            <!--<li><a href="#"><i class="social_twitter"></i></a></li>-->
                            <!--<li><a href="#"><i class="social_vimeo"></i></a></li>-->
                            <!--<li><a href="#"><i class="social_linkedin"></i></a></li>-->
                            <li><a href="https://wa.me/+212665686335"><i class="fab fa-whatsapp"></i></a></li>
                            <li><a href="https://www.youtube.com/channel/UCOf7kCKDptUQC9lIUWrmVnQ"><i
                                        class="social_youtube"></i></a></li>
                        </ul>
                    </div>
                </div>

                <div class="col-lg-5 col-sm-6">
                    <div class="f_widget link_widget pl_30 wow fadeInUp" data-wow-delay="0.2s">
                        <h3 class="f_title">المحاور</h3>

                        <ul class="list-unstyled link_list">
                            
                            <li>
                                <a
                                    href="/articles/thematiques?id=1">
                                    المسار التقني لسلاسل الإنتاج&#8230;</a>
                            </li>

                            
                            <li>
                                <a
                                    href="/articles/thematiques?id=3">
                                    ريادة الأعمال للفلاحين الشباب&#8230;</a>
                            </li>

                            
                            <li>
                                <a
                                    href="/articles/thematiques?id=4">
                                    مواجهة تغير المناخ /&#8230;</a>
                            </li>

                            
                            <li>
                                <a
                                    href="/articles/thematiques?id=2">
                                    التثمين والتسويق / التحفيزات&#8230;</a>
                            </li>

                                                    </ul>

                    </div>
                </div>
                <div class="col-lg-3 col-sm-6">
                    <div class="f_widget link_widget wow fadeInUp" data-wow-delay="0.4s">
                        <h3 class="f_title">الفئات</h3>

                        <ul class="list-unstyled link_list">
                            
                            <li>
                                <a
                                    href="/articles/categories?id=3">مقالات و بحوث   </a>
                            </li>

                            
                            <li>
                                <a
                                    href="/articles/categories?id=6">برامج اذاعية</a>
                            </li>

                            
                            <li>
                                <a
                                    href="/articles/categories?id=2">دليل المماراسات الجيدة</a>
                            </li>

                            
                            <li>
                                <a
                                    href="/articles/categories?id=5">المدونة الصوتية</a>
                            </li>

                            
                            <li>
                                <a
                                    href="/articles/categories?id=1">التقارير والمنشورات</a>
                            </li>

                            
                            <li>
                                <a
                                    href="/articles/categories?id=4">أشرطة فيديو / كتيبات رقمية</a>
                            </li>

                                                    </ul>
                    </div>
                </div>
                <div class="col-lg-3 col-sm-6">

                </div>
            </div>
            <div class="border_bottom"></div>
        </div>
    </div>
    <div class="footer_bottom text-center">
        <div class="container">
            <p> © 2024 جميع الحقوق محفوظة <a href="http://www.onca.gov.ma/"
                    target="_blank">ONCA</a></p>
        </div>
    </div>
</footer>
    </div>

    <!-- Back to top button -->
    <a id="back-to-top" title="Back to Top"></a>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://ardna.org/dist/js/jquery-3.2.1.min.js"></script>
    <script src="https://ardna.org/dist/js/pre-loader.js"></script>
    <script src="https://ardna.org/assets/bootstrap/js/popper.min.js"></script>
    <script src="https://ardna.org/assets/bootstrap/js/bootstrap.min.js"></script>
    <script src="https://ardna.org/assets/bootstrap/js/bootstrap-select.min.js"></script>
    <script src="https://ardna.org/assets/font-size/js/rv-jquery-fontsize-2.0.3.js"></script>
    <script src="https://ardna.org/dist/js/parallaxie.js"></script>
    <script src="https://ardna.org/dist/js/TweenMax.min.js"></script>
    <script src="https://ardna.org/dist/js/anchor.js"></script>
    <script src="https://ardna.org/dist/js/jquery.wavify.js"></script>
    <script src="https://ardna.org/assets/wow/wow.min.js"></script>
    <script src="https://ardna.org/assets/prism/prism.js"></script>
    <script src="https://ardna.org/assets/niceselectpicker/jquery.nice-select.min.js"></script>
    <script src="https://ardna.org/assets/mcustomscrollbar/jquery.mCustomScrollbar.concat.min.js"></script>
    <script src="https://ardna.org/assets/thdoan-magnify/js/jquery.magnify.js"></script>
    <script src="https://ardna.org/assets/counterup/jquery.counterup.min.js"></script>
    <script src="https://ardna.org/assets/counterup/jquery.waypoints.min.js"></script>
    <script src="https://ardna.org/dist/js/main.js"></script>


</body>

</html>"""
    
    scraper.scrape_articles(main_page_html)

if __name__ == "__main__":
    main()
from lxml import html
import requests

def fetch_html(link):
    try:
        response = requests.get(link)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        return f"Error fetching the page: {e}"

def save_html(html_content, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)
    except IOError as e:
        return f"Error writing to file: {e}"

def fetch_and_save_all_links(file_with_links):
    try:
        with open(file_with_links, 'r', encoding='utf-8') as file:
            links = file.readlines()

        results = []
        for index, link in enumerate(links, start=1):
            link = link.strip()  # Remove any extra whitespace or newline characters
            html_content = fetch_html(link)
            if html_content.startswith("Error"):
                results.append(html_content)
            else:
                filename = f"downloaded_page_{index}.html"
                save_result = save_html(html_content, filename)
                if save_result:
                    results.append(save_result)
                else:
                    results.append(f"HTML content saved to {filename}")

        return results
    except IOError as e:
        return f"Error reading file: {e}"


# file_with_links = "links.txt"
# result = fetch_and_save_all_links(file_with_links)
# print(result)



def extract_consequential_elements_from_file(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    tree = html.fromstring(html_content)
    
    consequential_elements = []
    selectors = [
        # link
        'a[href]',
        # button
        'button',
        '[role="button"]', '[role="radio"]', '[role="option"]', '[role="combobox"]'
        # input
        'input[type="button"]',
        'input[type="submit"]',
        'input[type="reset"]',
        'input[type="checkbox"]',
        'input[type="radio"]',
        'input[type="text"]',
        'input[type="password"]',
        'input[type="email"]',
        'input[type="file"]',
        # choosing
        'select',
        'option'
        'textarea',
        'form',
        '*[onclick]',
        '*[onchange]',
        '*[onsubmit]',
        '*[onmouseover]',
        '*[onmouseout]',
        '*[onkeydown]',
        '*[onkeyup]',
        '*[onkeypress]',
        '*[onfocus]',
        '*[onblur]',
        '*[onload]',
        '*[onunload]',
        # editable value
        '*[contenteditable="true"]',
        '*[draggable="true"]',
        # interactive features
        '*[tabindex]',
        '*[accesskey]'
    ]


    for selector in selectors:
        elements = tree.xpath(f'//{selector}')
        consequential_elements.extend(elements)

    return list(set(consequential_elements))

if __name__ == "__main__":

    html_file_path = 'example.html'  
    elements = extract_consequential_elements_from_file(html_file_path)
    for elem in elements:
        print(html.tostring(elem, pretty_print=True, encoding='unicode'))
    file_with_links = "links.txt"
    result = fetch_and_save_all_links(file_with_links)
    print(result)


def get_pagination_page_array(page, total_pages):
    """
    Return an array of page numbers to display for a given page with
    an offset around it.
    E.g with the current page page=4 and offset 2:
        [2,3,4,5,6]
    The total amount of pages is needed for boundary calculation.
    """
    first_page_to_show = page - 4
    last_page_to_show = page + 4

    first_page_offset = 0

    if first_page_to_show < 1:
        first_page_offset = first_page_to_show * -1 + 1
        first_page_to_show = 1

    if last_page_to_show > total_pages:
        if first_page_to_show > 1 and first_page_offset == 0:
            first_page_to_show = max(
                first_page_to_show - last_page_to_show + total_pages, 1
            )
        last_page_to_show = total_pages
    else:
        last_page_to_show = min(
            total_pages, last_page_to_show + first_page_offset
        )

    return list(range(first_page_to_show, last_page_to_show + 1))


def get_download_url(model, model_details):
    """
    Return the appropriate ubuntu.com/download url for the model

    :param model: a certifiedmodel resource
    :param model_details: a certifiedmodeldetails resource
    :return: appropriate ubuntu.com/download url
    """
    platform_category = model.get("category", "").lower()
    architecture = model_details.get("architecture", "").lower()

    if model_details.get("level") == "Enabled":
        # Enabled systems use oem images without download links.
        return

    if platform_category in ["desktop", "laptop"]:
        return "https://ubuntu.com/download/desktop"

    if "core" in platform_category:
        return "https://ubuntu.com/download/iot/"

    if "server" in platform_category:
        # Server platforms have special landing pages based on architecture.
        arch = ""
        if "arm" in architecture:
            arch = "arm"
        elif "ppc" in architecture:
            arch = "power"
        elif "s390x" in architecture:
            arch = "s390x"
        return f"https://ubuntu.com/download/server/{arch}"

    return "https://ubuntu.com/download"

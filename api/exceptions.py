from rest_framework.exceptions import APIException


class OutofStockException(APIException):
    status_code = 400
    default_detail = "Some of the products are out of stock.."


class InvaidSchemaException(APIException):
    status_code = 400
    default_detail = "Invalid product schema.."


class ProductDoesNotExistException(APIException):
    status_code = 400
    default_detail = "Product Does Not Exist.."

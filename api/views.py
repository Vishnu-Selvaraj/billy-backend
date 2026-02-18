from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User, Item, Invoice, InvoiceItem
from .serializers import (
    UserSerializer,
    ItemsSerializer,
    ResponseItemsSerializer,
    InvoiceCreateSerializer,
)

# Create your views here.


# Create new User
@api_view(["POST"])
@permission_classes((AllowAny,))
def addUser(request):
    try:
        data = request.data
        # print(data)
        name = data.get("customerName")
        discount = data.get("discount")
        newUser = User(full_name=name, discount=discount, username=name)
        newUser.save()
        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        )
    except Exception as e:
        print("Error occured in addUser func", {e})
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Get all Users
@api_view(["GET"])
@permission_classes((AllowAny,))
def getAllUsers(request):
    try:
        try:
            userData = User.objects.all()
        except User.DoesNotExist:
            return Response(
                {"message": "No Data Found", "data": []},
                status=status.HTTP_200_OK,
            )

        serializer = UserSerializer(userData, many=True)

        return Response(
            {"message": "Data Found", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        print("Error occured in getAllUsers func", {e})
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Add new Product


@api_view(["POST"])
@permission_classes((AllowAny,))
def createProduct(request):
    try:
        data = request.data
        item_name = data.get("itemName")
        price = data.get("price")
        if not item_name and not price:
            return Response(
                {"error": "Please fill all the fields."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        item_serializer = ItemsSerializer(data=request.data)
        if item_serializer.is_valid():
            item_serializer.save()
            return Response(
                {"message": "Product added successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": item_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        print("Error occured in createProduct func", {e})
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Get All Products


@api_view(["GET"])
@permission_classes((AllowAny,))
def getAllProducts(request):
    try:
        try:
            productData = Item.objects.all()
        except Item.DoesNotExist:
            return Response(
                {"message": "No Data Found", "data": []},
                status=status.HTTP_200_OK,
            )

        serialized_data = ResponseItemsSerializer(productData, many=True)
        # print(serialized_data.data)

        return Response(
            {"message": "Data Found", "data": serialized_data.data},
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        print("Error occured in getAllProducts func", {e})
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Create Invoice
@api_view(["POST"])
@permission_classes((AllowAny,))
def create_invoice(request):
    try:
        serializer = InvoiceCreateSerializer(data=request.data)
        if serializer.is_valid():
            invoice = serializer.save()
            return Response(
                {"message": "Invoice created successfully", "invoice_id": invoice.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("Error occured in create_invoice func", {e})
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Get All Invoices


@api_view(["GET"])
@permission_classes((AllowAny,))
def getAllInvoices(request):
    try:
        try:
            invoiceData = Invoice.objects.all().order_by("-id")
            if not invoiceData.exists():
                return Response(
                    {"message": "No Data Found", "data": []},
                    status=status.HTTP_200_OK,
                )
            responseData = []
            for data in invoiceData:
                responseData.append(
                    {
                        "invoice_id": data.id,
                        "customer_name": data.customer.full_name,
                        "date": data.date,
                        "discount": data.discount,
                        "items": data.discount,
                        "total": data.grand_total,
                    }
                )
            return Response(
                {"message": "Data Found", "data": responseData},
                status=status.HTTP_200_OK,
            )
        except Invoice.DoesNotExist:
            return Response(
                {"message": "No Data Found", "data": []},
                status=status.HTTP_200_OK,
            )

    except Exception as e:
        print("Error occured in getAllInvoices func", {e})
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Get Invoice Id


@api_view(["GET"])
@permission_classes((AllowAny,))
def getInvoiceById(request, invoice_id):
    try:
        try:
            invoice = (
                Invoice.objects.select_related("customer")
                .prefetch_related("invoice_items__item")
                .get(pk=invoice_id)
            )
        except Invoice.DoesNotExist:
            return Response(
                {"message": "Invoice not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        items = []
        for invoiceItem in invoice.invoice_items.all():
            items.append(
                {
                    "item_name": invoiceItem.item.item_name,
                    "quantity": invoiceItem.quantity,
                    "unit_price": str(invoiceItem.unit_price),
                    "line_total": str(invoiceItem.line_total),
                }
            )

        responseData = {
            "invoice_id": invoice.id,
            "customer_name": invoice.customer.full_name,
            "date": invoice.date,
            "discount": str(invoice.discount),
            "items": items,
            "grand_total": str(invoice.grand_total),
        }

        return Response(
            {"message": "Data Found", "data": responseData},
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        print("Error occured in getInvoiceById func", {e})
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

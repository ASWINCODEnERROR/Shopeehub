from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import stripe
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY






class PaymentView(APIView):
    def post(self,request,*args,**kwargs):
        amount = request.data.get('amount')
        token = request.data.get('token')
        
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='inr',
                source=token,
                description='Payment for Order'
            )
            return Response({'message':'Payment successfull'},status=200)
        except stripe.error.CardError as e:
            return Response({'error':str(e)},status=e.http_status)
        except Exception as e:
            return Response({'error':str(e)},status=500)





# class Payment_Class (APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self,request) :
#         try:
#             enroll_id = self.request.data['enroll_id']
#             type = self.request.data['type']
#             session = stripe.checkout.Session.create(
#             line_items=[{
#             'price_data': {
#                 'currency': 'USD',
#                 'product_data': {
#                 'name': self.request.data['name'],
#                 },
#                 'unit_amount': self.request.data['price'],
#             },
#             'quantity': 1 ,
#             }],
#             mode='payment',
#             # # success_url=self.request.data['origin_site'] + '/success=true&session_id={CHECKOUT_SESSION_ID}',
#             success_url=self.request.data['origin_site'] + '/success/{CHECKOUT_SESSION_ID}/' + str(enroll_id) + '/' + str(type),
#             cancel_url=self.request.data['origin_site'] + '/canceled=true/' + str(enroll_id) + '/' + str(type),
#             # # cancel_url=self.request.data['origin_site'] + '/canceled=true',

        
#             )

#             return Response({
#                 "status" : status.HTTP_200_OK,
#                 "message" : session
#             })

#         except Exception as e:
#             return Response({
#                 "status" : status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message" : str(e)
#             })

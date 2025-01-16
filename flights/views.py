from django.shortcuts import render
from .models import Flight, Airport, Passenger
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
  return render(request, "flights/index.html", {
    "flights": Flight.objects.all()
  })

def flight(request, flight_id):
  flight = Flight.objects.get(id = flight_id)
  passengers = flight.passengers.all()
  non_passengers = Passenger.objects.exclude(flights=flight).all()
  return render(request, "flights/flight.html",{
    "flight": flight,
    "passengers": passengers,
    "non_passengers": non_passengers
  })

def book(request, flight_id):
  if(request.method == "POST"):
    try:
      flight = Flight.objects.get(pk = flight_id)
      passenger_id = int(request.POST["passenger"])
      passenger = Passenger.objects.get(pk = passenger_id)
      passenger.flights.add(flight)
      return HttpResponseRedirect(reverse("flights:flight", args = (flight_id,)))
    except Flight.DoesNotExist:
            return render(request, "flights/flight.html", {
                "message": "Voo não encontrado.",
                "flight": None,
                "passengers": [],
                "non_passengers": Passenger.objects.all()
            })
    except Passenger.DoesNotExist:
            flight = Flight.objects.get(pk=flight_id)
            return render(request, "flights/flight.html", {
                "message": "Passageiro não encontrado.",
                "flight": flight,
                "passengers": flight.passengers.all(),
                "non_passengers": Passenger.objects.exclude(flights=flight).all()
            })
    except ValueError:
            flight = Flight.objects.get(pk=flight_id)
            return render(request, "flights/flight.html", {
                "message": "ID de passageiro inválido.",
                "flight": flight,
                "passengers": flight.passengers.all(),
                "non_passengers": Passenger.objects.exclude(flights=flight).all()
            })
    except Exception as e:
            flight = Flight.objects.get(pk=flight_id)
            return render(request, "flights/flight.html", {
                "message": f"Erro ao fazer reserva: {str(e)}",
                "flight": flight,
                "passengers": flight.passengers.all(),
                "non_passengers": Passenger.objects.exclude(flights=flight).all()
            })

def create_passenger(request):
  if request.method == "POST":
    try: 
      first = request.POST["first"]
      last = request.POST["last"] 

      if not first or not last:
        return render(request, "flight/create_passenger.html", {
          "message": "Nome e Sobrenome são obrigatórios"
        })
      
      passenger = Passenger.objects.create(first = first, last = last)

      flight_id = request.POST.get("flight_id")
      if flight_id:
        return HttpResponseRedirect(reverse("flights:flight", args=(flight_id,)))
      return HttpResponseRedirect(reverse("flights:index"))

    except Exception as e:
      return render(request, "flights/create_passenger.html", {
        "message": f"Erro ao criar passageiro: {str(e)}"
      })

  return render(request, "flights/create_passenger.html")
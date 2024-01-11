"use client";
import Autoplay from "embla-carousel-autoplay";
import * as React from "react";
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from "../ui/carousel";
import { Card, CardContent } from "../ui/card";

export function ClothesCarousel() {

    const plugin = React.useRef(
        Autoplay({ delay: 2000, stopOnInteraction: true })
      )
      
    return(
        <Carousel
        plugins={[plugin.current]}
        onMouseEnter={plugin.current.stop}
        onMouseLeave={plugin.current.reset}
        
      opts={{
        align: "center",
      }}
      className="w-full max-w-sm mx-auto md:max-w-2xl lg:max-w-4xl xl:max-w-6xl"
    >
      <CarouselContent>
        {Array.from({ length: 10 }).map((_, index) => (
          <CarouselItem key={index} className="md:basis-1/2 lg:basis-1/3">
            <div className="p-1">
              <Card>
                <CardContent className="flex aspect-square items-center justify-center p-6">
                  <span className="text-3xl font-semibold">{index + 1}</span>
                </CardContent>
              </Card>
            </div>
          </CarouselItem>
        ))}
      </CarouselContent>
    </Carousel>
    )
}
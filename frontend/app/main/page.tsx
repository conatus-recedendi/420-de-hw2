"use client";
import { subtitle, title } from "@/components/primitives";
import { userStore } from "@/store/userStore";
import { Button } from "@nextui-org/button";
import {
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Image,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ScrollShadow,
  Select,
  Skeleton,
} from "@nextui-org/react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import { useEffect } from "react";

const list = [
  {
    title: "Product 1",
    img: "https://source.unsplash.com/random/300x300",
    price: "$10",
  },
  {
    title: "Product 2",
    img: "https://source.unsplash.com/random/300x300",
    price: "$12",
  },
  {
    title: "Product 3",
    img: "https://source.unsplash.com/random/300x300",
    price: "$14",
  },
  {
    title: "Product 4",
    img: "https://source.unsplash.com/random/300x300",
    price: "$14",
  },
  {
    title: "Product 5",
    img: "https://source.unsplash.com/random/300x300",
    price: "$14",
  },
  {
    title: "Product 6",
    img: "https://source.unsplash.com/random/300x300",
    price: "$14",
  },
  {
    title: "Product 7",
    img: "https://source.unsplash.com/random/300x300",
    price: "$14",
  },
  {
    title: "Product 8",
    img: "https://source.unsplash.com/random/300x300",
    price: "$14",
  },
];
export default function Main() {
  // const params = useParams();
  const searchParams = useSearchParams();
  const { fetchPredict, recommendedCategory, openPopup, closeModal, user } =
    userStore();
  const router = useRouter();

  useEffect(() => {
    try {
      fetchPredict(user?.id.toString() ?? "");
    } catch {
      router.push("/");
    }
  }, []);

  const handleClickAction = () => {
    router.push(
      "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"
    );
  };

  return (
    <section className="flex flex-col items-center justify-center gap-4">
      <h1
        className={title({
          fullWidth: false,
          className: "self-start justify-start",
        })}
      >
        {searchParams.get("user")}님 이런 제품을 찾고 있나요?
      </h1>
      <p className={subtitle()}>
        좋아하실 만한 {recommendedCategory} 카테고리를 추천해드려요
      </p>
      <ScrollShadow
        hideScrollBar
        offset={100}
        orientation="horizontal"
        className="w-[100%] px-4"
      >
        <div className="flex flex-row gap-6 ">
          {list.map((item, index) => (
            <Card
              className=" min-w-[180px]"
              shadow="sm"
              key={index}
              isPressable
              onPress={() => console.log("item pressed")}
            >
              <CardBody className="overflow-visible p-2">
                <Image
                  shadow="sm"
                  radius="lg"
                  width="100%"
                  alt={item.title}
                  className="w-full object-cover h-[140px] "
                  src={item.img}
                />
              </CardBody>
              <CardFooter className="text-small justify-between">
                <b>{item.title}</b>
                <p className="text-default-500">{item.price}</p>
              </CardFooter>
            </Card>
          ))}
        </div>
      </ScrollShadow>
      <Card className="w-[100%] space-y-5 py-4 p-4">
        <Skeleton className="rounded-lg">
          <div className="h-60" />
        </Skeleton>
      </Card>
      <Card className="w-[100%] space-y-5 py-4 p-4">
        <Skeleton className="rounded-lg">
          <div className="h-[100vh]" />
        </Skeleton>
      </Card>
      <Modal size={"lg"} isOpen={openPopup} onClose={closeModal}>
        <ModalContent>
          <ModalHeader>이벤트 마케팅 팝업</ModalHeader>
          <ModalBody>
            <Card className="flex items-center justify-center gap-4">
              <CardHeader className="pb-0 pt-2 px-4 flex-col items-start">
                <p className="text-tiny uppercase font-bold">Daily Event</p>
                <small className="text-default-500">
                  2024.04.01 ~ 2024.04.01
                </small>
                <h4 className="font-bold text-large">
                  모든 제품군 90% 할인 혜택
                </h4>
              </CardHeader>
              <Image
                src="https://source.unsplash.com/random/300x300"
                alt="Discount"
                width="100%"
                height={200}
                className="object-cover"
              />
            </Card>
            <div>
              <p className="text-lg font-semibold">
                {user?.id}님을 위한 할인 혜택
              </p>
              <p>이벤트 마케팅을 위한 특별한 할인 혜택을 받으세요!</p>
              <p>지금 바로 할인을 받으려면 아래 버튼을 클릭하세요.</p>
            </div>
            {/* <p>이벤트 마케팅을 위한 특별한 할인 혜택을 받으세요!</p>ㄴ */}
          </ModalBody>
          <ModalFooter>
            <Button onClick={handleClickAction}>할인 받기</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </section>
  );
}

"use client";
import { Link } from "@nextui-org/link";
import { Snippet } from "@nextui-org/snippet";
import { Code } from "@nextui-org/code";
import { button as buttonStyles } from "@nextui-org/theme";
import { siteConfig } from "@/config/site";
import { title, subtitle } from "@/components/primitives";
import { GithubIcon } from "@/components/icons";
import { Select, SelectItem } from "@nextui-org/select";
import { Card, CardBody, CardFooter, CardHeader } from "@nextui-org/react";
import { Button } from "@nextui-org/button";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { userStore } from "@/store/userStore";

export default function Home() {
  const [selectedUserId, setSelectedUserId] = useState<null | string>(null);
  const router = useRouter();
  const { fetchUserList, userList, selectUser } = userStore();

  useEffect(() => {
    fetchUserList();
  }, []);

  const handleClickLogin = () => {
    if (selectedUserId) {
      selectUser(Number(selectedUserId));
      router.push(`/main?user=${selectedUserId}`);
    }
  };

  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      <div className="inline-block max-w-lg text-center justify-center">
        <h1 className={title()}>Login Page</h1>
        <br />
        <Card className={"my-8"}>
          <CardHeader>
            <p className={subtitle()}>DB 상에 존재하는 유저를 선택해주세요.</p>
          </CardHeader>
          <CardBody>
            <Select
              onChange={(e) => setSelectedUserId(e.target.value)}
              label="Login as User"
              placeholder="Select User"
              className="max-w-xs"
            >
              {userList.map((user) => (
                <SelectItem key={user.id} value={user.id.toString()}>
                  {user.id.toString()}
                </SelectItem>
              ))}
            </Select>
          </CardBody>
          <CardFooter className={"flex justify-center"}>
            {!selectedUserId ? (
              <Button color="default" disabled size="lg">
                Login
              </Button>
            ) : (
              <Button
                color="primary"
                variant="shadow"
                size="lg"
                onClick={handleClickLogin}
              >
                Login
              </Button>
            )}
          </CardFooter>
        </Card>
        <br />
      </div>
    </section>
  );
}
